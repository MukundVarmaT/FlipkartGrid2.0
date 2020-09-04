import audio_utils
import argparse
import os
import numpy as np
import glob
from tqdm import tqdm
import random
import yaml

parser = argparse.ArgumentParser("dataset script file")
parser.add_argument("--config_path", type=str, required=True, help="path to config file")
parser.add_argument("--output_dir", type=str, required=True, help="path to processed dir")
args = parser.parse_args()
config = yaml.safe_load(open(args.config_path, "r"))

def main():
    snr_lower = config["snr_lower"]
    snr_upper = config["snr_upper"]
    clean_dir = config["clean_dir"]
    noise_dir = config["noise_dir"]
    if not os.path.exists(clean_dir) or not os.path.exists(noise_dir):
        print("data directory doesn't exist. Exiting...")
        exit()
    silence_length = float(config["silence_length"])
    sampling_rate = int(config["sampling_rate"])
    audioformat = config["audioformat"]
    audio_length = float(config["audio_length"])
    processed_dir = args.output_dir
    num_files = config["num_files"]

    op_noisy1_dir = os.path.join(processed_dir, "noisy1")
    op_noisy2_dir = os.path.join(processed_dir, "noisy2")

    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    if not os.path.exists(op_noisy1_dir):
        os.makedirs(op_noisy1_dir)
    if not os.path.exists(op_noisy2_dir):
        os.makedirs(op_noisy2_dir)
        
    audio_length = int(audio_length*sampling_rate)
    cleanfilenames = glob.glob(os.path.join(clean_dir, audioformat))
    noisefilenames = glob.glob(os.path.join(noise_dir, audioformat))

    with tqdm(total=num_files) as pbar:
        for file_counter in range(num_files):
            f = np.random.randint(0, len(cleanfilenames)-1)
            clean, _ = audio_utils.audioread(cleanfilenames[f])
            while len(clean) < audio_length:
                ind_f = np.random.randint(0, len(cleanfilenames)-1)
                new_clean, _ = audio_utils.audioread(cleanfilenames[ind_f])
                clean = np.append(clean, np.zeros(int(sampling_rate*silence_length)))
                clean = np.append(clean, new_clean)
            
            noise_f = noisefilenames[np.random.randint(0, len(noisefilenames))]
            noise, _ = audio_utils.audioread(noise_f)
            while len(noise) < len(clean):
                ind_f = np.random.randint(0, len(noisefilenames)-1)
                new_noise, _ = audio_utils.audioread(noisefilenames[ind_f])
                noise = np.append(noise, np.zeros(int(sampling_rate*silence_length)))
                noise = np.append(noise, new_noise)
            noise = noise[0:len(clean)]

            random_snr = random.randint(snr_lower, snr_upper)
            clean_snr, noise_snr, noisy_snr = audio_utils.snr_mixer(clean=clean, noise=noise, snr=random_snr)
            clean_snr = clean_snr[0:audio_length]
            noise_snr = noise_snr[0:audio_length]
            noisy_snr = noisy_snr[0:audio_length]
            audio_utils.audiowrite(noisy_snr, sampling_rate, os.path.join(op_noisy1_dir, "noisy_" + str(file_counter)+"_"+str(random_snr)+".wav"))

            noise_f = noisefilenames[np.random.randint(0, len(noisefilenames))]
            noise, _ = audio_utils.audioread(noise_f)
            while len(noise) < len(clean):
                ind_f = np.random.randint(0, len(noisefilenames)-1)
                new_noise, _ = audio_utils.audioread(noisefilenames[ind_f])
                noise = np.append(noise, np.zeros(int(sampling_rate*silence_length)))
                noise = np.append(noise, new_noise)
            noise = noise[0:len(clean)]

            random_snr = random.randint(snr_lower, snr_upper)
            clean_snr, noise_snr, noisy_snr = audio_utils.snr_mixer(clean=clean, noise=noise, snr=random_snr)
            clean_snr = clean_snr[0:audio_length]
            noise_snr = noise_snr[0:audio_length]
            noisy_snr = noisy_snr[0:audio_length]
            audio_utils.audiowrite(noisy_snr, sampling_rate, os.path.join(op_noisy2_dir, "noisy_" + str(file_counter)+"_"+str(random_snr)+".wav"))
            pbar.update(1)            

if __name__ == "__main__":
    main()
