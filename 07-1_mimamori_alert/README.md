
<img src="https://github.com/anoken/MiMaMori_Alert/blob/master/image/main_abst.jpg" width="640">

## Movie
https://youtu.be/Bnx68C0GwCg

## hackster.io
https://m5stack.hackster.io/anoken2017/mimamori-alert-for-your-home-security-098b12

## Story

"MiMaMori Alert" is automatic security Camera for your home. Automatic learning without teacher images, and notify if something is visitor. You're not at home, but you can see your visitors and thieves.

## Algorithm

The feature vector obtained by the neural network is filtered in the time series direction.
The motion value between the average vector and the feature vector at the current time is calculated. 
This value is large if moving, and small if static.
<img src="https://github.com/anoken/MiMaMori_Alert/blob/master/image/NN.jpg" width="640">

## Demo instruction

This source code requires the MixPy option Numpy. Stores custom binaries.
Neural networks require a MobileNetV1 model with a weight of 0.5. This is also stored.
Write to M5StickV / UnitV with Kflash.

<img src="https://github.com/anoken/MiMaMori_Alert/blob/master/image/kmodel_gui.jpg" width="320">

