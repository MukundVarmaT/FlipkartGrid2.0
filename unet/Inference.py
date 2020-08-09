import warnings
warnings.filterwarnings("ignore")

#import custom libraries
from Denoiser_API import Enhance_Speech

#import system libraries
import os
import glob
import argparse
import requests
import json
from tqdm import tqdm
import numpy as np
import pandas as pd
from jiwer import wer

#Function to save predicted transcripts
def Save(response, file_name):
	if os.path.exists(os.getcwd() + "/Enhanced_Files/Predicted_Transcripts/") == False:
		os.mkdir(os.getcwd() + "/Enhanced_Files/Predicted_Transcripts/")

	file_name = os.getcwd() + "/Enhanced_Files/Predicted_Transcripts/" + file_name[:-4] + ".txt"

	with open(file_name, 'w') as outfile:
		json.dump(response, outfile)

#Function to generate transcript
def ASR(audio_sample):
	headers = {'Authorization': 'Token 3715119fd7753d33bedbd3c2832752ee7b0a10c7'}
	url = 'https://dev.liv.ai/liv_transcription_api/recordings/'
	files = {'audio_file' : open(audio_sample,'rb')}
	data = {'user' : '310' ,'language' : 'HI'}
	
	res = (requests.post(url, headers = headers, data = data, files = files)).json()
	return res

#Predict Function
def Predict(Files, sr, verbosity_option, asr):
	if os.path.exists(os.getcwd()+"/Enhanced_Files/") == False:
		os.mkdir(os.getcwd()+"/Enhanced_Files/")

	Inference_Time = []
	
	for test_sample in tqdm(Files):
		enhanced_sample, infer_time = Enhance_Speech(test_sample, sr, verbosity_option)
		if asr:
			res_predicted = ASR(enhanced_sample)
			Save(res_predicted, os.path.basename(enhanced_sample))
		Inference_Time.append(infer_time)

	Inference_Time = np.asarray(Inference_Time)

	print(" Minimum Inference Time : " , Inference_Time.min())
	print(" Maximum Inference Time : " , Inference_Time.max())
	print(" Average Inference Time : " , Inference_Time.mean())



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--input_file", help="path/to/noisy_file")
	parser.add_argument("--sr", default=16000, type=int, help="sampling_rate")
	parser.add_argument("-v","--verbose", help="show intermediate steps", action="store_true")
	parser.add_argument("--asr", default=False, type=bool, help="return transcripts")
	args = parser.parse_args()

	if os.path.exists(args.input_file) == False:
		print(f"Error!	Input File  - {args.input_file} -  does not exists...")

	inp = args.input_file
	sr = args.sr

	if os.path.isfile(inp):
		Files = [inp]
	elif os.path.isdir(inp):
		Files = [os.path. join(inp, file) for file in os.listdir(inp)]

	Predict(Files, sr, args.verbose, args.asr)
