import warnings
warnings.filterwarnings("ignore")


#import system_libraries
import os
import librosa
import time
import numpy as np
from numpy import save, load
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#import Deep_Learning Libraries
import torch
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence
from torch.utils import data
import torch.optim as optim
from torchsummary import summary

#import custom_libraries
from model import Model
from dataloader import Load_Data
from train import Train

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():

	#Load_Samples from Training_Folder
	#Noisy, Clean = Load_Data()

	Noisy = load('Noisy_Sample.npy', allow_pickle=True)
	Clean = load('Clean_Sample.npy', allow_pickle=True)

	Noisy_Valid = load('Noisy_Sample_Valid.npy', allow_pickle = True)
	Clean_Valid = load('Clean_Sample_Valid.npy', allow_pickle = True)

	print("Loaded Samples")

	#Test_Point : Print Clean & Noisy Sample Shapes
	print("Training Samples Shape : ")
	print(Noisy.shape, Clean.shape)

	print("Validation Samples Shape : ")
	print(Noisy_Valid.shape, Clean_Valid.shape)

	#Initialize Model Architecture
	model = Model()
	model = model.float()
	model.to(device)

	Noisy = torch.tensor(Noisy, device=device).float()
	Clean = torch.tensor(Clean, device=device).float()

	Noisy_Valid = torch.tensor(Noisy_Valid, device=device).float()
	Clean_Valid = torch.tensor(Clean_Valid, device=device).float()

	#Noisy_Train, Noisy_Test, Clean_Train, Clean_Test = train_test_split(Noisy, Clean, random_state = 0, test_size = 0.2)

	#print(Noisy_Train.shape, Noisy_Test.shape, Clean_Train.shape, Clean_Test.shape)

	Train_Dataset = data.TensorDataset(Noisy,Clean) # create your datset
	Train_Loader = data.DataLoader(Train_Dataset, batch_size=16) # create your dataloader

	Validation_Dataset = data.TensorDataset(Noisy_Valid,Clean_Valid) # create your datset
	Validate_Loader = data.DataLoader(Validation_Dataset, batch_size=16) # create your dataloader

	print("Starting Training")

	Train(model, Train_Loader, Validate_Loader)
	#Validate_Metrics(Validate_Loader)


main()
