import torch
from torch.utils.data import Dataset 
import utils
import audio_utils
import numpy as np
import random

class Audio(Dataset):
    def __init__(self, clean_files, noise_files, audio_length, sr=16000, silence_len=0.2, snr_lower=1, snr_upper=40):
        self.clean_files = clean_files
        self.noise_files = noise_files
        self.audio_length = audio_length
        self.sr = sr
        self.silence_len = silence_len
        self.snr_lower = snr_lower
        self.snr_upper = snr_upper
    
    def __getitem__(self, indx):
        noisy_1, noisy_2 = self.mix(self.clean_files[indx], self.audio_length)
        return torch.tensor(noisy_1), torch.tensor(noisy_2)

    def __len__(self):
        return len(self.clean_files)
    
    def mix(self, clean_file, audio_length):
        clean, _ = audio_utils.audioread(clean_file)
        while len(clean) < audio_length:
            ind_f = np.random.randint(0, len(self.clean_files)-1)
            new_clean, _ = audio_utils.audioread(self.clean_files[ind_f])
            clean = np.append(clean, np.zeros(int(self.sr*self.audio_length)))
            clean = np.append(clean, new_clean)
        
        noise_f = self.noise_files[np.random.randint(0, len(self.noise_files))]
        noise, _ = audio_utils.audioread(noise_f)
        while len(noise) < len(clean):
            ind_f = np.random.randint(0, len(self.noise_files)-1)
            new_noise, _ = audio_utils.audioread(self.noise_files[ind_f])
            noise = np.append(noise, np.zeros(int(self.sr*self.audio_length)))
            noise = np.append(noise, new_noise)
        noise = noise[0:len(clean)]

        random_snr = random.randint(self.snr_lower, self.snr_upper)
        clean_snr, noise_snr, noisy_snr = audio_utils.snr_mixer(clean=clean, noise=noise, snr=random_snr)
        clean_snr = clean_snr[0:audio_length]
        noise_snr = noise_snr[0:audio_length]
        noisy_snr = noisy_snr[0:audio_length]
        noisy_1 = noisy_snr

        noise_f = self.noise_files[np.random.randint(0, len(self.noise_files))]
        noise, _ = audio_utils.audioread(noise_f)
        while len(noise) < len(clean):
            ind_f = np.random.randint(0, len(self.noise_files)-1)
            new_noise, _ = audio_utils.audioread(self.noise_files[ind_f])
            noise = np.append(noise, np.zeros(int(self.sr*self.audio_length)))
            noise = np.append(noise, new_noise)
        noise = noise[0:len(clean)]

        random_snr = random.randint(self.snr_lower, self.snr_upper)
        clean_snr, noise_snr, noisy_snr = audio_utils.snr_mixer(clean=clean, noise=noise, snr=random_snr)
        clean_snr = clean_snr[0:audio_length]
        noise_snr = noise_snr[0:audio_length]
        noisy_snr = noisy_snr[0:audio_length]
        noisy_2 = noisy_snr
        
        return noisy_1, noisy_2
