#import system_libraries
import os
import numpy as np
from numpy import load, save
import librosa
from tqdm import tqdm
import sounddevice as sd

#import custom_libraries
from utils import Get_Data_From_File, Preprocess_Data, Play_Audio_From_Wav, Play_Audio_From_Numpy

#Initializing Training_Data Directories
Base_Path = os.getcwd()
Clean_Dir = Base_Path + "/Training_Data/CleanSpeech_training/"
Noisy_Dir = Base_Path + "/Training_Data/NoisySpeech_training/"

def Load_Data():

	Clean_Files_List = os.listdir(Clean_Dir)
	Noisy_Files_List = os.listdir(Noisy_Dir)

	X = []
	Y = []

	Count = 0

	for clean_file in tqdm(Clean_Files_List):
		for noisy_file in Noisy_Files_List:

			#Check if corresponding noisy file is being loaded
			if clean_file == noisy_file.split('_')[3]:

				#Get Clean & Noisy Mixed Samples from WAV file stored in local disk
				clean_sample , clean_sample_rate = Get_Data_From_File(Clean_Dir + clean_file)
				noise_sample, noise_sample_rate = Get_Data_From_File(Noisy_Dir + noisy_file)

				#print(clean_sample.shape, noise_sample.shape)

				#print("Playing Clean Sample")
				#Play_Audio_From_Numpy(clean_sample, 8000)

				#print("Playing Noise Sample")
				#Play_Audio_From_Numpy(noise_sample, 8000)

				#Preprocess raw samples : random sampling 65,536 elements
				Noisy_Sample , Clean_Sample = Preprocess_Data(noise_sample, clean_sample)

				#print(Noisy_Sample.shape, Clean_Sample.shape)

				#Appending Noisy_Samples to Input_Domain(X) & Clean_Samples to Output_Domain(Y)
				Y.append(Clean_Sample)
				X.append(Noisy_Sample)

	#Vectorizing Lists for speed enhancements & ease-of-use
	X = np.asarray(X)
	Y = np.asarray(Y)

	#saves final list to local disk : X - Noisy_Samples & Y - Clean_Samples
	save('Clean_Sample.npy', Y)
	save('Noisy_Sample.npy', X)

	return X,Y

#Load_Data()
