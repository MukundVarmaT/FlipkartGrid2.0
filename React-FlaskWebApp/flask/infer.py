import model
import torch
import numpy as np
import librosa
import os

sr = 16000

def write_wav(fname, audio, sr=16000):
    librosa.output.write_wav(fname, y=audio, sr=sr)

def read_wav(fname, sr=16000):
    audio, _ = librosa.load(fname, sr=sr, mono=True)
    return audio

def infer(denoiser, file_list):
    audio = read_wav(file_list[0], sr)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        raw = torch.tensor([audio], dtype=torch.float32, device=device)
        out = denoiser(raw)
        out = [np.squeeze(s.detach().cpu().numpy()) for s in out]

    write_wav(file_list[1], out[0], sr)
    write_wav(file_list[2], out[1], sr)

def ready(checkpoint_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    denoiser = model.Model().to(device)
    ckpt = torch.load(checkpoint_path, map_location=device)
    denoiser.load_state_dict(ckpt)
    return denoiser