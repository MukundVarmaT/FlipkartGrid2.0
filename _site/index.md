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

| Noisy input | predicted clean |predicted noise |  
|:---:|:---:|:---:|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noisy_1.mp3?token=ALIPQRDLRE6ZCCVTUHLX6BK7HACC2" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/clean_1.wav?token=ALIPQRAGTYSQKEBSJUKJM5C7HACGC" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noise_1.wav?token=ALIPQRBLTAPHVBPW36DXFH27HACN2" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noisy_2.mp3?token=ALIPQRDP4D2WPA3W7XO4BXK7HACWQ" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/clean_2.wav?token=ALIPQRDYTWV5SNLFNUSHU7S7HACGG" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noise_2.wav?token=ALIPQREE2I4WTRLKT4YWOMC7HACOA" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noisy_3.mp3?token=ALIPQRCTCNJITMOX6ABLJ627HACWS" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/clean_3.wav?token=ALIPQRBNDTLJGGIALQ5Z2HK7HACGK" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noise_3.wav?token=ALIPQRCKT525E76WSQ4IID27HACOE" controls preload></audio>|

<p class="text"><b>Handpicked harder samples</b></p>

| Noisy input | predicted clean |predicted noise |  
|:---:|:---:|:---:|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noisy_4.wav?token=ALIPQRACDJCSY6BYCIKMOY27HACWW" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/clean_4.wav?token=ALIPQRA36KQE5L3N5CSQ2227HACGM" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noise_4.wav?token=ALIPQRFQ3T2FHBFMVG2QTW27HACOI" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noisy_5.wav?token=ALIPQRABKL6GZ3V3CJXVEG27HACXY" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/clean_5.wav?token=ALIPQRGAJBQKAFFGQYHN5C27HACGQ" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noise_5.wav?token=ALIPQRB2DEDZLJGL46OPGKS7HACOM" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noisy_6.wav?token=ALIPQRFOF4QSIIYG6SDQV327HACX4" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/clean_6.wav?token=ALIPQRCOULL2EP4TSI7WDRS7HACHQ" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/1/noise_6.wav?token=ALIPQRD5XJV6FWBCPRXG7NS7HACOQ" controls preload></audio>|

## Other experiments

### Modified UNet (Directly predicts clean sample)

<p class="text"><b>Audio samples given by Flipkart</b></p>

| Noisy input | predicted clean | 
|:---:|:---:|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/noisy_1.mp3?token=ALIPQRANMM6H6TQCV6JY7SK7HADBM" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/clean_1.wav?token=ALIPQRF5ISHQBRFBU34LCMC7HAC4I" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/noisy_2.wav?token=ALIPQRD7GF4ZUTMQQXOX2E27HADBO" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/clean_2.wav?token=ALIPQRB5XXHY3XADNUDJJRS7HAC4M" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/noisy_3.wav?token=ALIPQRBDJDDAJYQXHZRKHK27HADBS" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/clean_3.wav?token=ALIPQRCM5XSUMYCTQQAIABK7HAC4O" controls preload></audio>|

<p class="text"><b>Samples from generated dataset</b></p>

| Noisy input | predicted clean | 
|:---:|:---:|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/noisy_4.wav?token=ALIPQREEXTMF2EJ3ZDYQT6S7HADBU" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/clean_4.wav?token=ALIPQRDNFMPDRKEJGBVRED27HAC4U" controls preload></audio>|
|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/noisy_5.wav?token=ALIPQRHUBUT6FBT52V262CK7HADBY" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/clean_5.wav?token=ALIPQRDLEUAHYEPEZVOLAJ27HAC4Y" controls preload></audio>|
|<audio src="[{{ site.url }}/assets/audio/2/noisy_6.wav](https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/noisy_6.wav?token=ALIPQRD6NRER4PUF2IHSAZ27HADE2)" controls preload></audio>|<audio src="https://raw.githubusercontent.com/MukundVarmaT/FlipkartGrid2.0/gh-pages/assets/audio/2/clean_6.wav?token=ALIPQRC2HZYRLCTR5IXHLT27HAC44" controls preload></audio>|