import warnings
warnings.filterwarnings("ignore")

#import custom libraries
from Denoiser_API import Enhance_Speech

#import system libraries
import os
from os import path
import argparse
import requests
import json
from pesq import pesq
from tqdm import tqdm
import numpy as np
import pandas as pd
from jiwer import wer

def Save(response, file_name, mode):
	if mode == 0:
		if path.exists(os.getcwd() + "/Enhanced_Files/Noisy_Transcripts/") == False:
			os.mkdir(os.getcwd() + "/Enhanced_Files/Noisy_Transcripts/")
		file_name = os.getcwd() + "/Enhanced_Files/Noisy_Transcripts/" + file_name[:-4] + ".txt"
	else:
		if path.exists(os.getcwd() + "/Enhanced_Files/Predicted_Transcripts/") == False:
			os.mkdir(os.getcwd() + "/Enhanced_Files/Predicted_Transcripts/")
		file_name = os.getcwd() + "/Enhanced_Files/Predicted_Transcripts/" + file_name[:-4] + ".txt"

	with open(file_name, 'w') as outfile:
		json.dump(response, outfile)


#if predict for a set of files in a directory
def WER():

	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--input_file", help="path/to/predicted_files_dir")
	parser.add_argument("-x","--data_frame", help="path/to/data_frame")
	args = parser.parse_args()

	if path.exists(args.input_file) == False:
		print(f"\033[91mError!\033[00m	\033[93mInput directory\033[00m - {args.input_file} -  \033[93mdoes not exists...\033[00m")
		return

	test_dir = os.path.dirname(args.input_file) + '/'

	WER_List = []
	Audio_ID_List = []

	df = pd.read_excel(args.data_frame)

	for file in tqdm(os.listdir(test_dir)):

		Audio_File_Name = file.split('_')[0]
		res_predicted = ASR(test_dir + file)

		Audio_ID_List.append(df.iloc[int(Audio_File_Name),0])

		wer_file = wer(df.iloc[int(Audio_File_Name),1], res_predicted['transcriptions'][0]['utf_text'])
		WER_List.append(wer_file)

	WER_List = np.asarray(WER_List)
	Audio_ID_List = np.asarray(Audio_ID_List)

	DF = pd.DataFrame({'Audio_ID':Audio_ID_List, 'WER':WER_List})
	print(DF)

	DF.to_csv("WER_Result.csv")

	print("	\033[93mMax WER      : \033[00m" , WER_List.max())
	print("	\033[93mMin WER      : \033[00m" , WER_List.min())
	print("	\033[93mAverage WER      : \033[00m" , WER_List.mean())


headers = {'Authorization': 'Token 3715119fd7753d33bedbd3c2832752ee7b0a10c7'}
url = 'https://dev.liv.ai/liv_transcription_api/recordings/'

def ASR(audio_sample):
	files = {'audio_file' : open(audio_sample,'rb')}
	data = {'user' : '310' ,'language' : 'HI'}
	
	res = (requests.post(url, headers = headers, data = data, files = files)).json()
	return res


WER()