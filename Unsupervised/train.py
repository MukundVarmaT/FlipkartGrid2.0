import model
import torch
import os
from torch.utils.data import DataLoader
import librosa
from glob import glob
import wandb
import audio_utils
import dataset
import numpy as np

class Trainer:
    def __init__(self, config):
        self.clean_files = sorted(glob(os.path.join(config["clean_dir"], "*.wav"))) 
        self.noise_files = sorted(glob(os.path.join(config["noise_dir"], "*.wav")))
        self.output_dir = config["output_dir"]
        self.config = config

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.device = torch.device("cuda")
        self.model = model.UNet().to(self.device)
        train_dataset = dataset.Audio(self.clean_files, self.noise_files, config["audio_length"], config["sampling_rate"], config["silence_len"], config["snr_lower"], config["snr_upper"])
        self.train_dataloader = DataLoader(train_dataset, batch_size=config["batch_size"], shuffle=True, num_workers=config["num_workers"])
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=config["lr"], betas=(0.9,0.999))
        self.criterion = torch.nn.L1Loss()
    
    def train(self, epoch):
        for indx, (noisy_1, noisy_2) in enumerate(self.train_dataloader):
            noisy_1 = noisy_1.to(self.device)
            noisy_2 = noisy_2.to(self.device)
            out = self.model(noisy_1)
            loss = self.criterion(out, noisy_2)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            log = {"loss": loss.item()}
            wandb.log(log)
            if indx % self.config["eval_every"] == 0 and indx != 0:
                self.validate("{}_{}".format(epoch, indx))
    
    def validate(self, name):
        try:
            noisy, _ = next(self.val_iter)
        except:
            self.val_iter = iter(self.train_dataloader)
            noisy, _ = next(self.val_iter)
        audio_utils.write_wav(os.path.join(self.output_dir, "noisy_{}.wav".format(name)), noisy)
        wandb.log({"noisy": [wandb.Audio(os.path.join(self.output_dir, "noisy_{}.wav".format(name)), caption="noisy", sample_rate=16000)]})

        with torch.no_grad():
            m = noisy.mean()
            noisy = (noisy - m)
            noisy = torch.tensor([noisy]).to(self.device)
            out = self.model(noisy)
        
        clean = np.squeeze(out.cpu().detach().numpy())
        clean = clean + m
        audio_utils.write_wav(os.path.join(self.output_dir, "clean_{}.wav".format(name)), clean)
        wandb.log({"clean": [wandb.Audio(os.path.join(self.output_dir, "clean_{}.wav".format(name)), caption="clean", sample_rate=16000)]})
        torch.save(self.model.state_dict(), os.path.join(self.output_dir, "{}.pth".format(name)))

    def run(self):
        for epoch in range(self.config["epochs"]):
            self.train(epoch)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="path to config file")
    args = parser.parse_args()

    import yaml
    network_config = yaml.safe_load(open(args.config, "r"))
    trainer = Trainer(network_config)
    trainer.run()

