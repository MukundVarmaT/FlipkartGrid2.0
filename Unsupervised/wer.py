import pandas as pd
from jiwer import wer
import jiwer
import os
from glob import glob
import json 

data = pd.read_excel("original.xlsx")
wer_score = []
transcript_files = sorted(glob(os.path.join("transcripts", '*.txt')))
audio_id = []

for i in range(len(transcript_files)):
    f = os.path.basename(transcript_files[i]).split(".")[0]
    orig = data["Transcription "][int(f)]
    orig = orig.replace("@", "")
    orig = orig.replace("_", "")
    orig = orig.strip()
    if orig != "":
        f = open(transcript_files[i],"r") 
        tr = json.load(f) 
        pred = tr["transcriptions"][0]["utf_text"]
        pred = pred.replace("@", "")
        pred = pred.replace("_", "")
        orig = orig.strip()

        transformation = jiwer.Compose([
        jiwer.Strip(),
        jiwer.SentencesToListOfWords(),
        jiwer.RemoveEmptyStrings()
        ])
        error = wer(orig, pred,truth_transform=transformation,hypothesis_transform=transformation)
        wer_score.append(error)
        audio_id.append(f)
        # exit()
print("min: {}, mean: {}, max: {}".format(min(wer_score), sum(wer_score)/len(wer_score), max(wer_score)))

wer_result = pd.DataFrame()
wer_result["ID"] = audio_id
wer_result["WER"] = wer_score
wer_result.to_csv("WER_result.csv", index=False, header=True)
