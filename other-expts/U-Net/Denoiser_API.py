#import system_libraries
import os
import time
from numpy import save

#import Deep_Learning Libraries
import torch
import torch.nn as nn

#impot custom_libraries
from Model import Model
from utils import Get_Data_From_File, Save_Sample_To_Disk	

#Function to predict the ehanced waveform
def Predict(test_sample, model):
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	#Load Test_Sample as tensor of data_type float
	test_sample = torch.tensor(test_sample, device = device).float()

	#Reshape Test_Sample
	test_sample = test_sample.reshape(1, 1, -1) #[1,1,T]

	padded_length = 0

	if test_sample.size(-1) % 16384 != 0:   #Creates Chunks of size 16,384. Pads with zero if necessary.
		padded_length = 16384 - (test_sample.size(-1) % 16384)
		test_sample = torch.cat([test_sample, torch.zeros(1, 1, padded_length, device=device)], dim=-1)

	assert test_sample.size(-1) % 16384 == 0 and test_sample.dim() == 3
	test_sample_chunks = list(torch.split(test_sample, 16384, dim=-1))

	enhanced_chunks = []
	for chunk in test_sample_chunks:
		enhanced_chunks.append(model(chunk).detach().cpu())

	enhanced = torch.cat(enhanced_chunks, dim=-1)  # [1, 1, T]
	enhanced = enhanced if padded_length == 0 else enhanced[:, :, :-padded_length]

	enhanced = enhanced.reshape(-1)

	return enhanced


#Main Function to Enhance Speech
def Enhance_Speech(test_sample, sr, verbosity_option):

	if os.path.exists(os.getcwd()+"/Enhanced_Files/Enhanced_Audio/") == False:
		os.mkdir(os.getcwd()+"/Enhanced_Files/Enhanced_Audio/")
	Save_Dir = os.getcwd()+"/Enhanced_Files/Enhanced_Audio/"

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	Save_Name = os.path.splitext(os.path.basename(test_sample))[0] + "_Enhanced.wav"

	#Load Model Architecture & saved weights
	model = Model()
	model.load_state_dict(torch.load("Model_Epoch_200.pth", map_location = device))
	model = model.float()
	model.to(device)
	model.eval()

	test_sample, test_sample_rate = Get_Data_From_File(test_sample, sr)

	start_enhance_time = time.time()

	#Predcit Enhanced Sample
	Enhanced_Sample = Predict(test_sample, model)

	Enhanced_Sample = Enhanced_Sample.cpu().detach().numpy()

	end_enhance_time = time.time()

	#print("Saving Enhanced.wav to disk")
	Save_Sample_To_Disk(Save_Dir + Save_Name, Enhanced_Sample, test_sample_rate)

	if verbosity_option:
		print("Inference Time : " , end_enhance_time - start_enhance_time)

	return Save_Dir+Save_Name, end_enhance_time - start_enhance_time