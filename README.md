# Flipkart Grid 2.0 - Noise Suppresion Challenge

**Team name**: Comrades

**Team members**: K.Vikas Mahender, Mukund Varma T, Mukesh V

- Our proposed solution's audio samples can be found in this [link](https://mukundvarmat.github.io/FlipkartGrid2.0/)
- Solution Description - [video file]()

## Best model (extracts the speech and noise seperately from the mixture)

- WER scores - [CSV](./seperation/WER_result.csv) - **Avg WER: 0.565**
- Denoised samples for given data can be found [here](seperation/denoised/)
- Transcripts for the denoised samples can be found [here](seperation/transcripts)

**To run inference code on best model**:

`python3 seperation/infer.py --input <file/folder> --output <output-folder>`

other options

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
  --output OUTPUT  path to output folder
```

# Other experiments

## UNet Model (predicts clean samples from the mixture)

- WER scores - [CSV](./enhancement/WER_result.csv) - **Avg WER: 0.768**
- Denoised samples for given data can be found [here](enhancement/denoised/)
- Transcripts for the denoised samples can be found [here](enhancement/transcripts)

**To run inference code**:

`python3 enhancement/infer.py --i <file/folder>`

other options

```
usage: infer.py [-h] [-i INPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        path/to/noisy_file_dir

```

**Note: All training scripts and other model files can be found in the respective folders**


