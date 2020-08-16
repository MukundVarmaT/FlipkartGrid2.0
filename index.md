<h1 align="center">
<p>Flipkart Grid 2.0 Noise Suppression Challenge</p>
</h1>

<p class="text">
<b>Team name</b>: Comrades <br>
<b>Team members</b>: K Vikas Mahendar, Mukund Varma T, Mukesh V <br>
<b>College</b>: IIT Madras
</p>

<p class="text">Given are noisy audio samples along with the corresponding denoised output from the model. We include samples from our best model along with other experiments as well. The samples are hand-picked by us to showcase our model's capability.</p>

## 🎧 Model samples

### Best Model (seperates into clean and noise)

<p class="text"><b>Audio samples given by Flipkart</b></p>

| Noisy input | predicted clean | predicted noise |  
|:---:|:---:|:---:|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noisy_1.mp3?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/clean_1.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noise_1.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noisy_2.mp3?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/clean_2.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noise_2.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noisy_3.mp3?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/clean_3.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noise_3.wav?raw=true" controls preload></audio>|

<p class="text"><b>Handpicked harder samples</b></p>

| Noisy input | predicted clean |predicted noise |  
|:---:|:---:|:---:|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noisy_4.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/clean_4.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noise_4.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noisy_5.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/clean_5.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noise_5.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noisy_6.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/clean_6.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/1/noise_6.wav?raw=true" controls preload></audio>|

## Other experiments

### Modified UNet (Directly predicts clean sample)

<p class="text"><b>Audio samples given by Flipkart</b></p>

| Noisy input | predicted clean | 
|:---:|:---:|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/noisy_1.mp3?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/clean_1.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/noisy_2.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/clean_2.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/noisy_3.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/clean_3.wav?raw=true" controls preload></audio>|

<p class="text"><b>Samples from generated dataset</b></p>

| Noisy input | predicted clean | 
|:---:|:---:|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/noisy_4.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/clean_4.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/noisy_5.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/clean_5.wav?raw=true" controls preload></audio>|
|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/noisy_6.wav?raw=true" controls preload></audio>|<audio src="https://github.com/MukundVarmaT/grid-samples/blob/master/2/clean_6.wav?raw=true" controls preload></audio>|