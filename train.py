import model
import torch
import os
from glob import glob
import dataloader
import torch.optim as optim
import random
import numpy as np
from audio_utils import read_wav, write_wav
import wandb

def sisnr(x, s, eps=1e-8):
    def l2norm(mat, keepdim=False):
        return torch.norm(mat, dim=-1, keepdim=keepdim)
    x_zm = x - torch.mean(x, dim=-1, keepdim=True)
    s_zm = s - torch.mean(s, dim=-1, keepdim=True)
    t = torch.sum(x_zm * s_zm, dim=-1,keepdim=True) * s_zm / (l2norm(s_zm, keepdim=True)**2 + eps)
    loss = 20 * torch.log10(eps + l2norm(t) / (l2norm(x_zm - t) + eps))
    return loss

class Trainer:
    def __init__(self, network_config):
        # model and other params
        model_params = network_config["model_params"]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("running on device: ", self.device)
        self.model = model.Model(*model_params.values()).to(self.device)
        print("Model initialised, number of params : {}M".format(sum(p.numel() for p in self.model.parameters())/1e6))
        self.optimizer = optim.Adam(self.model.parameters(), lr=network_config["lr"], weight_decay=network_config["weight_decay"])
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optimizer, mode="min", factor=network_config["factor"], patience=network_config["patience"], min_lr=network_config["min_lr"])

        # set up dataloaders
        audio_format = network_config["audio_format"]
        self.noisy_files = sorted(glob(os.path.join(network_config["noisy_dir"], "*"+audio_format)))
        self.clean_files = sorted(glob(os.path.join(network_config["clean_dir"], "*"+audio_format)))
        self.noise_files = sorted(glob(os.path.join(network_config["noise_dir"], "*"+audio_format)))
        print("populated files. count: {}".format(len(self.noisy_files)))

        self.sr = network_config["sampling_rate"]
        self.audio_dataset = dataloader.Audio(self.noisy_files, self.clean_files, self.noise_files, self.sr)
        self.train_dataloader = dataloader.AudioLoader(self.audio_dataset, num_workers=network_config["num_workers"], chunk_size=network_config["chunk_size"], batch_size=network_config["batch_size"])

        # others
        self.step = 0
        self.num_epochs = network_config["num_epochs"]
        self.loss_counter = []
        self.step_every = network_config["step_every"]
        self.save_every = network_config["save_every"]
        self.output_dir = network_config["output_dir"]
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def train(self):
        self.model.train()

        for sample in self.train_dataloader:
            self.step+=1
            noisy, clean, noise = sample["noisy"].to(self.device), sample["clean"].to(self.device), sample["noise"].to(self.device)

            sep_clean, sep_noise = self.model(noisy.float())
            loss = torch.stack([sisnr(sep_clean, clean), sisnr(sep_noise, noise)])
            loss = torch.max(loss, dim=0)[0]
            loss = -torch.sum(loss)/len(noisy)

            loss.backward()
            self.optimizer.step()

            self.loss_counter.append(loss.item())
            log = {"loss": loss.item()}
            wandb.log(log)

            if self.step%self.save_every == 0:
                torch.save(self.model.state_dict(), os.path.join(self.output_dir, "{}.tar".format(self.step)))
                self.valid(self.step)
            if len(self.loss_counter)%self.step_every == 0:
                last_100 = sum(self.loss_counter[-100:])/100
                self.scheduler.step(last_100)

        print("\n")

    def valid(self, step):
        self.model.eval()
        index = random.randint(0, len(self.noisy_files)-1)
        noisy = dataloader.read_wav(self.noisy_files[index])
        write_wav(os.path.join(self.output_dir, "noisy_{}.wav".format(step)), noisy)

        wandb.log({"noisy": [wandb.Audio(os.path.join(self.output_dir, "noisy_{}.wav".format(step)), caption="noisy", sample_rate=self.sr)]})

        noisy = torch.tensor([noisy], dtype=torch.float32, device=self.device)
        with torch.no_grad():
            clean, noise = self.model(noisy)

        clean = np.squeeze(clean.cpu().detach().numpy())
        write_wav(os.path.join(self.output_dir, "clean_{}.wav".format(step)), clean, self.sr)
        wandb.log({"clean": [wandb.Audio(os.path.join(self.output_dir, "clean_{}.wav".format(step)), caption="clean", sample_rate=self.sr)]})
        
        noise = np.squeeze(noise.cpu().detach().numpy())
        write_wav(os.path.join(self.output_dir, "noise_{}.wav".format(step)), noise, self.sr)
        wandb.log({"noise": [wandb.Audio(os.path.join(self.output_dir, "noise_{}.wav".format(step)), caption="noise", sample_rate=self.sr)]})

    def run(self):
        wandb.init(project="flipkart-grid")
        print("started training!")
        for epoch in range(self.num_epochs):
            self.train()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="path to config file")
    args = parser.parse_args()

    import yaml
    network_config = yaml.safe_load(open(args.config, "r"))
    trainer = Trainer(network_config)
    trainer.run()