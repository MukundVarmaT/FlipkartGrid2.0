import numpy as np
import librosa
import soundfile as sf
import os

def write_wav(fname, audio, sr=16000):
    librosa.output.write_wav(fname, y=audio, sr=sr)

def read_wav(fname, sr=16000):
    audio, _ = librosa.load(fname, sr=sr, mono=True)
    return audio

def audioread(path, norm=True, start=0, stop=None):
    path = os.path.abspath(path)
    try:
        x, sampling_rate = sf.read(path, start=start, stop=stop)
    except RuntimeError:
        print('WARNING: Audio type not supported') 

    if len(x.shape) == 1:
        if norm:
            rms = (x ** 2).mean() ** 0.5
            scalar = 10 ** (-25 / 20) / (rms)
            x = x * scalar
    else:
        x = x.T
        x = x.sum(axis=0)/x.shape[0]
        if norm:
            rms = (x ** 2).mean() ** 0.5
            scalar = 10 ** (-25 / 20) / (rms)
            x = x * scalar
    return x, sampling_rate

def snr_mixer(clean, noise, snr):
    # Normalizing to -25 dB FS
    rmsclean = (clean**2).mean()**0.5
    scalarclean = 10 ** (-25 / 20) / rmsclean
    clean = clean * scalarclean
    rmsclean = (clean**2).mean()**0.5

    rmsnoise = (noise**2).mean()**0.5
    scalarnoise = 10 ** (-25 / 20) /rmsnoise
    noise = noise * scalarnoise
    rmsnoise = (noise**2).mean()**0.5
    
    # Set the noise level for a given SNR
    noisescalar = np.sqrt(rmsclean / (10**(snr/20)) / rmsnoise)
    noisenewlevel = noise * noisescalar
    noisyspeech = clean + noisenewlevel
    return clean, noisenewlevel, noisyspeech

def audiowrite(data, sampling_rate, destpath):
    destpath = os.path.abspath(destpath)
    sf.write(destpath, data, sampling_rate)