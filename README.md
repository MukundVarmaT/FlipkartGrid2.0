# Flipkart Grid 2.0 - Noise Suppresion Challenge

**Team name**: Comrades

**Team members**: K.Vikas Mahender, Mukund Varma T, Mukesh V

- Our proposed solution's audio samples can be found in this [link]()
- Solution Description - [video file]()

## Best model (extracts the speech and noise seperately from the mixture)

WER scores - [CSV]()
Denoised samples for given data can be found [here]()

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

WER scores - [CSV]()
Denoised samples for given data can be found [here]()

**Note: All training scripts and other model files can be found in the respective folders**


