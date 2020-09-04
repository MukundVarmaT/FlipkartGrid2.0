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

### Conv-TasNet - supervised (Best Model) (seperates into clean and noise)

<p class="text"><b>Different noise types to model real life urban environments</b></p>

<style>
audio { width: 200px; }
</style>

| Type | Noisy input | Predicted clean | Predicted noise |  
|:---:|:---:|:---:|:---:|
| Street Traffic |<audio src="{{ site.url }}/assets/audio/1.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/1_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/1_noise.wav" controls preload></audio>|
| Baby crying |<audio src="{{ site.url }}/assets/audio/2.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/2_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/2_noise.wav" controls preload></audio>|
| Noisy Crowd |<audio src="{{ site.url }}/assets/audio/3.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/3_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/3_noise.wav" controls preload></audio>|
| Secondary speaker |<audio src="{{ site.url }}/assets/audio/4.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/4_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/4_noise.wav" controls preload></audio>|
| Piano Music |<audio src="{{ site.url }}/assets/audio/5.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/5_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/5_noise.wav" controls preload></audio>|
| Television |<audio src="{{ site.url }}/assets/audio/6.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/6_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/6_noise.wav" controls preload></audio>|
| Construction |<audio src="{{ site.url }}/assets/audio/7.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/7_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/7_noise.wav" controls preload></audio>|
| Airport Announcement |<audio src="{{ site.url }}/assets/audio/8.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/8_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/8_noise.wav" controls preload></audio>|
| C4E Tech (Tamil) + Music |<audio src="{{ site.url }}/assets/audio/9.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/9_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/9_noise.wav" controls preload></audio>|
| Linus Tech Tips (English) + Music |<audio src="{{ site.url }}/assets/audio/10.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/10_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/10_noise.wav" controls preload></audio>|
| Flipkart Ad (Hindi) + Music |<audio src="{{ site.url }}/assets/audio/11.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/11_clean.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/11_noise.wav" controls preload></audio>|

### Simple U-Net model trained using an unsupervised scheme

<p class="text"><b>Samples from a model trained from scratch to validate our unsupervised training proceedure.</b></p>

| Noisy input | Predicted clean (supervised) | Predicted clean (unsupervised) |  
|:---:|:---:|:---:|
|<audio src="{{ site.url }}/assets/audio/12.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/12_sup.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/12_unsup.wav" controls preload></audio>|
|<audio src="{{ site.url }}/assets/audio/13.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/13_sup.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/13_unsup.wav" controls preload></audio>|
|<audio src="{{ site.url }}/assets/audio/14.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/14_sup.wav" controls preload></audio>|<audio src="{{ site.url }}/assets/audio/14_unsup.wav" controls preload></audio>|

