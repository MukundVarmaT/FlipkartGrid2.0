#import system_libraries
import numpy as np
import librosa
import soundfile as sf

#Function to load audio_sample in python
def Get_Data_From_File(File, sr):
	sample, sample_rate = librosa.load(File, mono = True)
	return sample, sample_rate

#Function to preprocess audio_sample : randomly sample 16,384 elements from audio_file
def Preprocess_Data(data_a, data_b):
	sample_length = 16384

	assert len(data_a) == len(data_b), "Inconsistent dataset length, unable to sampling"
	assert len(data_a) >= sample_length, f"len(data_a) is {len(data_a)}, sample_length is {sample_length}."

	frames_total = len(data_a)

	start = np.random.randint(frames_total - sample_length + 1)
	end = start + sample_length

	return data_a[start:end], data_b[start:end]

#Function to save audio_sample to local_disk
def Save_Sample_To_Disk(Path, Sample, Sample_Rate):
	#print(len(Sample))
	librosa.output.write_wav(Path, Sample, Sample_Rate)
	return 0