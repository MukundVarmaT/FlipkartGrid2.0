import model
import torch
import numpy as np
from audio_utils import read_wav, write_wav
import os
from glob import glob
from pesq import pesq
import time
from table_logger import TableLogger
import json
import requests
import warnings
warnings.filterwarnings("ignore")
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ckpt", default="best.pth", type=str, help="path to checkpoint")
parser.add_argument("--input", required=True, type=str, help="path to input folder/file")
parser.add_argument("--sr", default=16000, type=int, help="sampling_rate")
parser.add_argument("--format", default="*wav", type=str, help="audio format")
parser.add_argument("--output", default="denoised", type=str, help="path to output folder")
args = parser.parse_args()

if __name__ == "__main__":

    checkpoint_path = args.ckpt
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    denoiser = model.Model().to(device)
    ckpt = torch.load(checkpoint_path)
    denoiser.load_state_dict(ckpt)

    print("Loading saved model from {}".format(checkpoint_path))
    print("Model initialised, number of params : {}M".format(sum(p.numel() for p in denoiser.parameters())/1e6))

    sr = args.sr
    inp = args.input
    if os.path.isdir(inp):
        noisy_files = sorted(glob(os.path.join(inp, args.format)))
    elif os.path.isfile(inp):
        noisy_files = [inp]
    else:
        raise Exception("given input file/directory does not exist please check path")
    output_dir = args.output
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    time_counter = []
    pesq_counter = []
    tb = TableLogger(columns="FILE,TIME (secs),PESQ",float_format='{:,.2f}'.format, default_colwidth=15)

    for f in noisy_files:
        audio = read_wav(f, sr)
        start = time.time()
        with torch.no_grad():
            raw = torch.tensor([audio], dtype=torch.float32, device=device)
            out = denoiser(raw)
            out = [np.squeeze(s.detach().cpu().numpy()) for s in out]
        
        t = time.time() - start
        score = pesq(sr, out[0], audio, 'wb')
        time_counter.append(t)
        pesq_counter.append(score)
        tb(os.path.basename(f).split(".")[0], t, score)
	    
        write_wav(os.path.join(output_dir, os.path.basename(f).split(".")[0] + "_clean.wav"), out[0], sr)
        write_wav(os.path.join(output_dir, os.path.basename(f).split(".")[0] + "_noise.wav"), out[1], sr)

    print("\n")
    print("Time stats: min: {:.2f} mean: {:.2f} max: {:.2f}".format(min(time_counter), sum(time_counter)/len(time_counter), max(time_counter)))
    print("PESQ stats: min: {:.2f} mean: {:.2f} max: {:.2f}".format(min(pesq_counter), sum(pesq_counter)/len(pesq_counter), max(pesq_counter)))