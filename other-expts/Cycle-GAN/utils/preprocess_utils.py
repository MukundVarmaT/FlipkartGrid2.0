import argparse
import pickle
import librosa
import pyworld
import numpy as np
import os

num_mcep = 24
sampling_rate = 16000
frame_period = 5.0

def load_wave(path, sampling_rate):
    wave, _ = librosa.load(path, sr=sampling_rate, mono=True)
    return wave

def decompose(wave, sampling_rate, frame_period=5.0):
    wave = wave.astype(np.float64)
    fund_freq, timeaxis = pyworld.harvest(wave, sampling_rate, frame_period=frame_period, f0_floor=71.0, f0_ceil=800.0)
    spect = pyworld.cheaptrick(wave, fund_freq, timeaxis, sampling_rate)
    aperiod = pyworld.d4c(wave, fund_freq, timeaxis, sampling_rate)
    return fund_freq, timeaxis, spect, aperiod

def decode_spectral_envelop(coded_spect, sampling_rate):
    fftlen = pyworld.get_cheaptrick_fft_size(sampling_rate)
    decoded_spect = pyworld.decode_spectral_envelope(coded_spect, sampling_rate, fftlen)
    return decoded_spect

def speech_synthesis(fund_freq, decoded_spect, aperiod, sampling_rate, frame_period):
    wav = pyworld.synthesize(fund_freq, decoded_spect, aperiod, sampling_rate, frame_period)
    wav = wav.astype(np.float32)
    return wav

def encode_spectral_envelop(spect, sampling_rate, dim=24):
    coded_spect = pyworld.code_spectral_envelope(spect, sampling_rate, dim)
    return coded_spect

def encode_data(wave, sampling_rate, frame_period, coded_dim):
    fund_freq, timeaxis, spect, aperiod = decompose(wave, sampling_rate, frame_period)
    coded_spect = encode_spectral_envelop(spect, sampling_rate, coded_dim)
    return fund_freq, timeaxis, spect, aperiod, coded_spect

def process_file(folder, filename):
    path = os.path.join(folder,filename)
    wave = load_wave(path, sampling_rate)
    fund_freq, timeaxis, spect, aperiod, coded_spect = encode_data(wave, sampling_rate, frame_period, num_mcep)
    return fund_freq, timeaxis, spect, aperiod, coded_spect

def pitch_conversion(fund_freq, mean_log_src, std_log_src, mean_log_target, std_log_target):
    fund_freq_conv = np.exp((np.log(fund_freq) - mean_log_src) / std_log_src * std_log_target + mean_log_target)
    return fund_freq_conv

def wav_padding(wav, sr, frame_period, multiple=4):
    assert wav.ndim == 1
    num_frames = len(wav)
    num_frames_padded = int((np.ceil((np.floor(num_frames / (sr * frame_period / 1000)) + 1) / multiple + 1) * multiple - 1) * (sr * frame_period / 1000))
    num_frames_diff = num_frames_padded - num_frames
    num_pad_left = num_frames_diff // 2
    num_pad_right = num_frames_diff - num_pad_left
    wav_padded = np.pad(wav, (num_pad_left, num_pad_right), 'constant', constant_values=0)
    return wav_padded