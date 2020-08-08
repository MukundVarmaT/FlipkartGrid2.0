import numpy as np
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.dataloader import default_collate
import random
from audio_utils import read_wav, write_wav

class Audio(Dataset):
    def __init__(self, noisy_files, clean_files, noise_files, sample_rate=8000):
        self.noisy_files = noisy_files
        self.clean_files = clean_files
        self.noise_files = noise_files
        self.sr = sample_rate
    def __len__(self):
        return len(self.noisy_files)
    def __getitem__(self, index):
        noisy, clean, noise = read_wav(self.noisy_files[index]), read_wav(self.clean_files[index]), read_wav(self.noise_files[index])
        return {"noisy":noisy, "clean":clean, "noise":noise}

class ChunkSplitter:
    def __init__(self, chunk_size, least=16000):
        self.chunk_size = chunk_size
        self.least = least
    def _make_chunk(self, sample, s):
        chunk = dict()
        chunk["noisy"] = sample["noisy"][s:s + self.chunk_size]
        chunk["clean"] = sample["clean"][s:s + self.chunk_size]
        chunk["noise"] = sample["noise"][s:s + self.chunk_size]
        return chunk
    def split(self, sample):
        N = sample["noisy"].size
        if N < self.least:
            return []
        chunks = []
        if N < self.chunk_size:
            P = self.chunk_size - N
            chunk = dict()
            chunk["noisy"] = np.pad(sample["noisy"], (0, P), "constant")
            chunk["clean"] = np.pad(sample["clean"], (0, P), "constant")
            chunk["noise"] = np.pad(sample["noise"], (0, P), "constant")
            chunks.append(chunk)
        else:
            s = random.randint(0, N % self.least)
            while True:
                if s + self.chunk_size > N:
                    break
                chunk = self._make_chunk(sample, s)
                chunks.append(chunk)
                s += self.least
        return chunks

class AudioLoader(object):
    def __init__(self, dataset, num_workers=4, chunk_size=32000, batch_size=16):
        self.batch_size = batch_size
        self.splitter = ChunkSplitter(chunk_size, least=chunk_size // 2)
        self.audio_loader = DataLoader(dataset, batch_size=batch_size // 2, num_workers=num_workers, shuffle=True, collate_fn=self._collate)
    def _collate(self, batch):
        chunk = []
        for sample in batch:
            chunk += self.splitter.split(sample)
        return chunk
    def _merge(self, chunk_list):
        N = len(chunk_list)
        random.shuffle(chunk_list)
        blist = []
        for s in range(0, N - self.batch_size + 1, self.batch_size):
            batch = default_collate(chunk_list[s:s + self.batch_size])
            blist.append(batch)
        rn = N % self.batch_size
        return blist, chunk_list[-rn:] if rn else []
    def __iter__(self):
        chunk_list = []
        for chunks in self.audio_loader:
            chunk_list += chunks
            batch, chunk_list = self._merge(chunk_list)
            for obj in batch:
                yield obj