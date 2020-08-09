# Flipkart Grid 2.0 - Noise Suppresion Challenge

**Team name**: Comrades

**Team members**: K.Vikas Mahender, Mukund Varma T, Mukesh V

**College name**: IIT Madras

- Our proposed solution's audio samples can be found in this [link](https://mukundvarmat.github.io/FlipkartGrid2.0/)
- Solution Description - [video file](https://drive.google.com/file/d/1Ndksb6eApeIUo3d-Z3kFmVsqRcp-LA1y/view?usp=sharing)

## Best model (extracts the primary speaker and background noise seperately from the mixture)

- WER scores - [CSV](./best_model/WER_result.csv)- **Avg WER: 0.565**
- Denoised samples for given data can be found [here](https://drive.google.com/file/d/1Ctr6S-LT3-dIeO9RUpxM1DM20QI-EUgP/view?usp=sharing)
- Transcripts for the denoised samples can be found [here](./best_model/transcripts/)

**To run inference code on best model**:

`python3 best_model/infer.py --input <file/folder> --output <output-folder>`

returns two outputs for every given input, labelled as clean and noise respectively in the output folder. For other options

```
usage: infer.py [-h] [--ckpt CKPT] --input INPUT [--asr ASR] [--sr SR]
                [--format FORMAT] --output OUTPUT
optional arguments:
  -h, --help       show this help message and exit
  --ckpt CKPT      path to checkpoint (default best.pth)
  --input INPUT    path to input folder/file
  --asr ASR        flag for asr on/off (default False)
  --sr SR          sampling_rate (default 16000)
  --format FORMAT  audio format (default *.wav)
  --output OUTPUT  path to output folder (default ./output/)
```

------

# Other experiments

## UNet Model (predicts clean samples from the mixture)

- WER scores - [CSV](./unet/WER_result.csv) - **Avg WER: 0.729**
- Denoised samples for given data can be found [here](https://drive.google.com/file/d/1A-eaDtCRtO5XfE3AhqtF23tXAQcAlexM/view?usp=sharing)
- Transcripts for the denoised samples can be found [here](./unet/transcripts/)

**To run inference code**:

`python3 unet/Inference.py -i <file/folder>`

other options

```
usage: Inference.py [-h] [-i INPUT_FILE] [--sr SR] [-v]
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        path/to/noisy_file
  --sr SR               sampling_rate
  -v, --verbose         show intermediate steps
```

**Note: All training scripts and other model files can be found in the respective folders for each model**

## To run the flask server

React + Flask WebApp to integrate proposed solution into an end-to-end pipeline. 

```bash
cd Flask/flask
pip3 install -r requirements.txt
python3 server.py
```
