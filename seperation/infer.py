import model
import torch
import numpy as np
from audio_utils import read_wav, write_wav
import os
from glob import glob
import time
import json
import requests
import warnings
warnings.filterwarnings("ignore")
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ckpt", default="best.pth", type=str, help="path to checkpoint")
parser.add_argument("--input", required=True, type=str, help="path to input folder/file")
parser.add_argument("--asr", default=False, type=bool, help="flag for asr on/off")
parser.add_argument("--sr", default=16000, type=int, help="sampling_rate")
parser.add_argument("--format", default="*wav", type=str, help="audio format")
parser.add_argument("--output", required=True, type=str, help="path to output folder")
args = parser.parse_args()

def ASR(audio_sample):
    headers = {'Authorization': 'Token 3715119fd7753d33bedbd3c2832752ee7b0a10c7'}
    data = {'user' : '310' ,'language' : 'HI'}
    files = {'audio_file' : open(audio_sample,'rb')}
    url = 'https://dev.liv.ai/liv_transcription_api/recordings/'
    res = (requests.post(url, headers = headers, data = data, files = files)).json()
    return res

if __name__ == "__main__":

    checkpoint_path = args.ckpt
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    denoiser = model.Model().to(device)
    ckpt = torch.load(checkpoint_path)
    denoiser.load_state_dict(ckpt)

    print("Loading saved model from {}".format(checkpoint_path))
    print("Model initialised, number of params : {}M".format(sum(p.numel() for p in denoiser.parameters())/1e6))

    inp = args.input
    output = args.output
    if not os.path.exists(output):
        os.makedirs(output)
    audio_out = os.path.join(output, "audio")
    if not os.path.exists(audio_out):
        os.makedirs(audio_out)
    if args.asr:
        trans_out = os.path.join(output, "transcripts")
        if not os.path.exists(trans_out):
            os.makedirs(trans_out)

    sr = args.sr

    if os.path.isdir(inp):
        noisy_files = sorted(glob(os.path.join(inp, args.format)))
    elif os.path.isfile(inp):
        noisy_files = [inp]
    else:
        raise Exception("given input file/directory does not exist please check path")

    if len(noisy_files) == 0:
        raise Exception("folder does not contain files of format {}".format(args.format))
    
    time_counter = []

    for f in noisy_files:
        audio = read_wav(f, sr)

        start = time.time()
        with torch.no_grad():
            raw = torch.tensor([audio], dtype=torch.float32, device=device)
            out = denoiser(raw)
            out = [np.squeeze(s.detach().cpu().numpy()) for s in out]

        t = time.time() - start
        time_counter.append(t)
        print("processed file {} in {:.2f} secs".format(os.path.basename(f), t))
        write_wav(os.path.join(audio_out, os.path.basename(f).split(".")[0] + "_clean.wav"), out[0], sr)
        write_wav(os.path.join(audio_out, os.path.basename(f).split(".")[0] + "_noise.wav"), out[1], sr)

        if args.asr:
            transcript = ASR(os.path.join(audio_out, os.path.basename(f).split(".")[0] + "_clean.wav"))
            with open(os.path.join(trans_out, os.path.basename(f).split(".")[0] + ".json"), 'w') as outfile:
                json.dump(transcript, outfile)
        exit()

    print("Time stats: min: {:.2f} mean: {:.2f} max: {:.2f}".format(min(time_counter), sum(time_counter)/len(time_counter), max(time_counter)))