from torch.utils.data.dataset import Dataset
import torch
import numpy as np
import os
from utils import preprocess_utils
import random

class dataset(Dataset):
    def __init__(self, noisy_dir, clean_dir, n_frames):
        self.noisy_dir = noisy_dir
        self.clean_dir = clean_dir
        self.noisy_files = os.listdir(noisy_dir)
        self.clean_files = os.listdir(clean_dir)
        self.n_frames = n_frames
    
    def __getitem__(self, index):
        random.shuffle(self.noisy_files)
        random.shuffle(self.clean_files)
        noisy_file = self.noisy_files[index]
        clean_file = self.clean_files[index]
        _, _, _, _, noisy_coded_spect = preprocess_utils.process_file(self.noisy_dir, noisy_file)
        _, _, _, _, clean_coded_spect = preprocess_utils.process_file(self.clean_dir, clean_file)

        noisy = self.select_frames(noisy_coded_spect.T)
        clean = self.select_frames(clean_coded_spect.T)
        return noisy, clean

    def select_frames(self, coded_spect):
        frames_total = coded_spect.shape[1]
        assert frames_total >= self.n_frames
        start = np.random.randint(frames_total - self.n_frames + 1)
        end = start + self.n_frames
        return coded_spect[:, start:end]

    def __len__(self):
        return min(len(self.noisy_files), len(self.clean_files))
