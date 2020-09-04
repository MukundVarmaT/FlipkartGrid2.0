 #import system_libraries
import os
import time
import numpy as np
from tqdm import tqdm
from numpy import save, load
import matplotlib.pyplot as plt

#import Deep_Learning Libraries : Pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import data
import torch.optim as optim
from torchsummary import summary
from torch.utils.tensorboard import SummaryWriter

#import custom_libraries
from utils import Play_Audio_From_Numpy
from dataloader import Load_Data

#Set Device : CPU/GPU for training model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#tensorboard initialization
writer = SummaryWriter()

def Validate(model, validateloader):
	running_loss = 0
	samples = 0

	Loss = nn.MSELoss()

	for i, data in tqdm(enumerate(validateloader, 0)):
		noisy, clean = data[0].to(device), data[1].to(device)

		clean = clean.reshape(clean.shape[0],-1)
		noisy = noisy.reshape(noisy.shape[0],1,-1)

		model.eval()
		enhanced = model(noisy)
		enhanced = enhanced.reshape(enhanced.shape[0],-1)

		loss = Loss(clean, enhanced)
		running_loss += loss.item()
		samples += clean.size(0)

		#print("Running_Loss : " , Running_Loss , " ::::: Samples : " ,Samples)

	Val_Loss = running_loss / samples
	mosel = model.train()
	return Val_Loss

def Train(model, trainloader, validateloader):

	#Directory to Save Models & Loss Plots
	Model_Dir = os.getcwd() + "/MSNSD_Models/"
	Fig_Dir = os.getcwd() + "/Training_Figures/"

	Epochs = 200  #Train 100 epochs
	#print("Total Number of Samples to train : ", Samples)

	#Initializing Adam Optimizer
	optimizer = optim.Adam(model.parameters(), lr=0.0001, betas=(0.9, 0.999))

	#Mean_Squared_Error Loss for penalizing predicted samples
	Loss = nn.MSELoss()

	#Initializing Learning Rate Scheduler
	scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, verbose=True)

	Loss_List = []
	Epoch_List = []
	Val_Loss_List = []

	for epoch in range(Epochs):

		start_epoch_time = time.time()

		Running_Loss = 0
		Samples = 0

		for i, input_data in tqdm(enumerate(trainloader, 0)):
			noisy, clean = input_data[0].to(device), input_data[1].to(device)

			#print("Playing Clean Sample")
			#Play_Audio_From_Numpy(clean.detach().cpu().numpy().reshape(-1), 8000)

			#print("Playing Noise Sample")
			#Play_Audio_From_Numpy(noise.detach().cpu().numpy().reshape(-1), 8000)

			#print("Playing noisy Sample")
			#Play_Audio_From_Numpy(noisy.detach().cpu().numpy().reshape(-1), 8000)

			#Reshape Clean & Noisy sample to shape : [1,1,T]
			clean = clean.reshape(clean.shape[0],-1)
			noisy = noisy.reshape(noisy.shape[0],1,-1)

			#Load Clean & Noisy sample as tensor of data_type float
			noisy = torch.tensor(noisy, device = device).float()
			clean = torch.tensor(clean, device = device).float()
			
			#Train the sample_pair
			optimizer.zero_grad()

			#Forward_Propagation
			enhanced = model(noisy)
			enhanced = enhanced.reshape(enhanced.shape[0],-1)

			#print(noisy.shape, clean.shape, enhanced.shape)

			#Compute MSE_Loss
			loss = Loss(clean, enhanced)

			#Backward_Propagation
			loss.backward()
			optimizer.step()

			Samples += clean.size(0)

			#Loss
			Running_Loss += loss.item()

			#print("Running_Loss : " , Running_Loss , " ::::: Samples : " ,Samples)

		#Total_Loss at the end of epoch
		Epoch_Loss = Running_Loss / Samples #Mean of individual losses of each batch of samples

		end_epoch_time = time.time()

		Val_Loss = Validate(model, validateloader)

		#scheduler.step(Val_Loss)

		#Save Model every 10 epochs
		if (epoch+1) % 1 == 0:
			Model_Name = "Model_Epoch_" + str(epoch+1) + ".pth"
			print("Saving Model : ", Model_Name)
			torch.save(model.state_dict(), Model_Dir + Model_Name)

		print("Epoch :\033[93m %2.0f \033[00m::::: Loss :\033[91m % 5.20f \033[00m::::: Validation_Loss :\033[91m % 5.20f \033[00m::::: Epoch Time :\033[34m % 5.5f \033[00m" %(epoch+1,(Epoch_Loss), (Val_Loss), (end_epoch_time-start_epoch_time)))

		writer.add_scalar('Loss/train', Epoch_Loss, epoch+1)
		writer.add_scalar('Loss/val', Val_Loss, epoch+1)


