import argparse
import pickle
import torch
import numpy as np
import model
import dataloader
from utils import common, preprocess_utils
import os
import librosa
import torch.backends.cudnn as cudnn

parser = argparse.ArgumentParser(description="Train model")
parser.add_argument('--noisy_dir', type=str,  required=True, help="path to dir A")
parser.add_argument('--clean_dir', type=str,  required=True, help="path to dir B")
parser.add_argument('--model_save', type=str,  required=True, help="path to model save")
parser.add_argument('--output_save', type=str,  required=True, help="path to output save")
parser.add_argument("--log", type=str, help="path to log")
parser.add_argument('--config', type=str, required=True, help="config path")
parser.add_argument("--wandb", type=bool, help="Wandb on/off")

args = parser.parse_args()
network_config = common.parse_yaml(args.config)

if args.wandb == True:
    import wandb
    wandb.init(project="flipkart-grid-gan")
elif args.log!= None:
    if not os.path.exists(args.log):
        os.makedirs(args.log)
else:
    print("Exiting... choose either wandb or provide path to logs")
    exit()

if not os.path.exists(args.output_save):
    os.makedirs(args.output_save)
if not os.path.exists(args.model_save):
    os.makedirs(args.model_save)

class CycleGANTrain:
    def __init__(self, args, network_config):
        self.start_epoch = 0
        self.num_epochs = network_config["num_epochs"]
        self.batch_size = network_config["batch_size"]
        self.noisy_dir = args.noisy_dir
        self.clean_dir = args.clean_dir
        self.wandb = args.wandb
        if self.wandb == None:
            from torch.utils.tensorboard import SummaryWriter
            self.writer = SummaryWriter(args.log)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)
        
        self.generator_noisy2clean = model.Generator().to(self.device)
        self.generator_clean2noisy = model.Generator().to(self.device)
        self.discriminator_noisy = model.Discriminator().to(self.device)
        self.discriminator_clean = model.Discriminator().to(self.device)
        cudnn.benchmark = True
        cudnn.fastest = True

        mse_loss = torch.nn.MSELoss()
        g_params = list(self.generator_noisy2clean.parameters()) + list(self.generator_clean2noisy.parameters())
        d_params = list(self.discriminator_noisy.parameters()) + list(self.discriminator_clean.parameters())

        self.generator_lr = network_config["generator_lr"]
        self.discriminator_lr = network_config["discriminator_lr"]
        self.decay_iter = network_config["decay_iter"]

        self.generator_lr_decay = self.generator_lr / self.decay_iter
        self.discriminator_lr_decay = self.discriminator_lr / self.decay_iter
        self.start_decay = network_config["start_decay"]
        self.cycle_loss_lambda = network_config["cycle_loss_lambda"]
        self.identity_loss_lambda = network_config["identity_loss_lambda"]
        self.identity_loss_stop = network_config["identity_loss_stop"]

        self.generator_optim = torch.optim.Adam(g_params, lr=self.generator_lr, betas=(0.5, 0.999))
        self.discriminator_optim = torch.optim.Adam(d_params, lr=self.discriminator_lr, betas=(0.5, 0.999))

        self.model_dir = args.model_save
        self.output_dir = args.output_save
        self.generator_loss = []
        self.discriminator_loss = []

    def adjust_lr_rate(self, optimizer, name):
        if name == 'generator':
            self.generator_lr = max(0., self.generator_lr - self.generator_lr_decay)
            for param_groups in optimizer.param_groups:
                param_groups['lr'] = self.generator_lr
        else:
            self.discriminator_lr = max(0., self.discriminator_lr - self.discriminator_lr_decay)
            for param_groups in optimizer.param_groups:
                param_groups['lr'] = self.discriminator_lr

    def train(self):
        n_samples = min(len(os.listdir(self.noisy_dir)), len(os.listdir(self.clean_dir)))
        print("started training")
        for epoch in range(self.start_epoch, self.num_epochs):
            torch.cuda.empty_cache()
            self.generator_clean2noisy.train()
            self.generator_noisy2clean.train()
            self.discriminator_clean.train()
            self.discriminator_noisy.train()
            dataset = dataloader.dataset(self.noisy_dir, self.clean_dir, n_frames=128)
            train_loader = torch.utils.data.DataLoader(dataset=dataset, batch_size=self.batch_size, shuffle=True, drop_last=False, num_workers=1)
            for i, (noisy, clean) in enumerate(train_loader):
                num_iterations = (n_samples//self.batch_size)*epoch + i
                if num_iterations > self.identity_loss_stop:
                    self.identity_loss_lambda = 0
                if num_iterations > self.start_decay:
                    self.adjust_lr_rate(self.generator_optim, name="generator")
                    self.adjust_lr_rate(self.discriminator_optim, name="discriminator")
                
                # do some stuff with the noisy data!
                noisy = noisy.to(self.device).float()
                fake_clean = self.generator_noisy2clean(noisy)
                d_fake_clean = self.discriminator_clean(fake_clean)
                cycle_noisy = self.generator_clean2noisy(fake_clean)
                d_cycle_noisy = self.discriminator_noisy(cycle_noisy)
                identity_noisy = self.generator_clean2noisy(noisy)
                
                clean = clean.to(self.device).float()
                fake_noisy = self.generator_clean2noisy(clean)
                d_fake_noisy = self.discriminator_noisy(fake_noisy)
                cycle_clean = self.generator_noisy2clean(fake_noisy)
                d_cycle_clean = self.discriminator_clean(cycle_clean)
                identity_clean = self.generator_noisy2clean(clean)

                cycle_loss = torch.mean(torch.abs(noisy - cycle_noisy)) + torch.mean(torch.abs(clean - cycle_clean))
                identity_loss = torch.mean(torch.abs(noisy - identity_noisy)) + torch.mean(torch.abs(clean - identity_clean))

                g_forward_noisy2clean = torch.mean((1-d_fake_clean)**2)
                g_backward_clean2noisy = torch.mean((1-d_cycle_noisy)**2)
                g_forward_clean2noisy = torch.mean((1-d_fake_noisy)**2)
                g_backward_noisy2clean = torch.mean((1-d_cycle_clean)**2)
                generator_loss_noisy2clean = (g_forward_noisy2clean + g_backward_noisy2clean) / 2.0
                generator_loss_clean2noisy = (g_forward_clean2noisy + g_backward_clean2noisy) / 2.0
                generator_loss = generator_loss_noisy2clean + generator_loss_clean2noisy + self.cycle_loss_lambda*cycle_loss + self.identity_loss_lambda*identity_loss
                self.generator_loss.append(generator_loss.item())

                self.generator_optim.zero_grad()
                self.discriminator_optim.zero_grad()
                generator_loss.backward()
                self.generator_optim.step()

                d_real_noisy = self.discriminator_noisy(noisy)
                d_real_clean = self.discriminator_clean(clean)
                fake_clean = self.generator_noisy2clean(noisy)
                fake_noisy = self.generator_clean2noisy(clean)
                d_fake_noisy = self.discriminator_noisy(fake_noisy)
                d_fake_clean = self.discriminator_clean(fake_clean)
                
                d_loss_noisy_real = torch.mean((1 - d_real_noisy) ** 2)
                d_loss_noisy_fake = torch.mean((0 - d_fake_noisy) ** 2)
                d_loss_noisy = (d_loss_noisy_real + d_loss_noisy_fake) / 2.0
                d_loss_clean_real = torch.mean((1 - d_real_clean) ** 2)
                d_loss_clean_fake = torch.mean((0 - d_fake_clean) ** 2)
                d_loss_clean = (d_loss_clean_real + d_loss_clean_fake) / 2.0
                d_loss = (d_loss_noisy + d_loss_clean) / 2.0
                self.discriminator_loss.append(d_loss.item())
                
                self.generator_optim.zero_grad()
                self.discriminator_optim.zero_grad()
                self.generator_optim.zero_grad()
                d_loss.backward()
                self.discriminator_optim.step()
                
                if self.wandb:
                    log = {"Generator Loss": generator_loss.item(),
                            "Discriminator Loss" : d_loss.item(),
                            "Noisy2Clean": generator_loss_noisy2clean,
                            "Clean2Noisy": generator_loss_clean2noisy,
                            "Identity Loss": identity_loss,
                            "Cycle Loss": cycle_loss,
                            "D Loss Noisy": d_loss_noisy,
                            "D Loss Clean": d_loss_clean}
                    wandb.log(log)
                else:
                    log = {"Generator Loss": generator_loss.item(),
                            "Discriminator Loss" : d_loss.item()}
                    self.writer.add_scalars("logging/G,D-loss/", log, num_iterations)
                    log = {"Noisy2Clean": generator_loss_noisy2clean,
                            "Clean2Noisy": generator_loss_clean2noisy}
                    self.writer.add_scalars("Logging/conv-loss/", log, num_iterations)
                    log = { "Identity Loss": identity_loss,
                            "Cycle Loss": cycle_loss}
                    self.writer.add_scalars("Logging/other-loss/", log, num_iterations)
                    log = {"D Loss Noisy": d_loss_noisy,
                            "D Loss Clean": d_loss_clean}
                    self.writer.add_scalars("Logging/d-loss/", log, num_iterations)

            msg = "Iter:{}\t Generator Loss:{:.4f} Discrimator Loss:{:.4f} \tGA2B:{:.4f} GB2A:{:.4f} G_id:{:.4f} G_cyc:{:.4f} D_A:{:.4f} D_B:{:.4f}".format(num_iterations, generator_loss.item(), d_loss.item(), generator_loss_noisy2clean, generator_loss_clean2noisy, identity_loss, cycle_loss, d_loss_noisy, d_loss_clean)
            msg = f"{common.bcolors.RED}{msg}{common.bcolors.ENDC}"
            print("{}".format(msg))
                
            if epoch%5 == 0 and epoch !=0:
                self.save_model_ckpt(epoch, "{}.tar".format(os.path.join(self.model_dir, str(epoch))))
                print(f"{common.bcolors.GREEN}MODEL SAVED!{common.bcolors.GREEN}")
                self.valid(epoch)
                
    def save_model_ckpt(self, epoch, PATH):
        torch.save({
            'epoch': epoch,
            'generator_loss_store': self.generator_loss,
            'discriminator_loss_store': self.discriminator_loss,
            'model_gennoisy2clean_state_dict': self.generator_noisy2clean.state_dict(),
            'model_genclean2noisy_state_dict': self.generator_clean2noisy.state_dict(),
            'model_discriminatornoisy': self.discriminator_noisy.state_dict(),
            'model_discriminatorclean': self.discriminator_clean.state_dict(),
            'generator_optimizer': self.generator_optim.state_dict(),
            'discriminator_optimizer': self.discriminator_optim.state_dict()
        }, PATH)

    
    def valid(self, epoch):
        num_mcep = 24
        sampling_rate = 16000
        frame_period = 5.0
        n_frames = 128
        self.generator_noisy2clean.eval()

        files = os.listdir(self.noisy_dir)
        indx = np.random.randint(0, len(files)-1)
        
        path = os.path.join(self.noisy_dir, files[indx])
        wave = preprocess_utils.load_wave(path, sampling_rate)
        librosa.output.write_wav(path=os.path.join(self.output_dir, str(epoch) + "_noisy.wav"), y=wave, sr=sampling_rate)
        if self.wandb:
            wandb.log({"NOISY-input": [wandb.Audio(wave, caption="noisy", sample_rate=sampling_rate)]})

        wave = preprocess_utils.wav_padding(wave, sampling_rate, frame_period, multiple=4)
        fund_freq, timeaxis, spect, aperiod, coded_spect = preprocess_utils.encode_data(wave, sampling_rate, frame_period, num_mcep)
        coded_spect = np.array([coded_spect.T])

        if torch.cuda.is_available():
            coded_spect = torch.from_numpy(coded_spect).cuda().float()
        else:
            coded_spect = torch.from_numpy(coded_spect).float()

        clean_spect = self.generator_noisy2clean(coded_spect)
        clean_spect = clean_spect.cpu().detach().numpy()
        clean_spect = np.squeeze(clean_spect)
        clean_spect = clean_spect.T
        clean_spect = np.ascontiguousarray(clean_spect).astype("double")

        decoded_clean = preprocess_utils.decode_spectral_envelop(clean_spect, sampling_rate)
        wave_clean = preprocess_utils.speech_synthesis(fund_freq, decoded_clean, aperiod, sampling_rate, frame_period)
        librosa.output.write_wav(path=os.path.join(self.output_dir, str(epoch) + "_clean.wav"), y=wave_clean, sr=sampling_rate)
        if self.wandb:
            wandb.log({"CLEAN-output": [wandb.Audio(wave_clean, caption="clean", sample_rate=sampling_rate)]})
    
if __name__ == "__main__":
    cyclegan = CycleGANTrain(args, network_config)
    cyclegan.train()