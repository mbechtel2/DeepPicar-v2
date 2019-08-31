# DeepPicar

<p align="center"><img src="https://github.com/mbechtel2/DeepPicar-v2/blob/master/images/DeepPicar.jpg" width="360" height="360"/></p>

DeepPicar is a low-cost autonomous RC car platform using a deep
convolutional neural network (CNN). DeepPicar is a small scale replication
of NVIDIA's real self-driving car called Dave-2, which drove on public
roads using a CNN. DeepPicar uses the same CNN architecture of NVIDIA's
Dave-2 and can drive itself in real-time locally on a Raspberry Pi 3.

Video:

[![DeepPicar Driving](http://img.youtube.com/vi/SrS5iQV2Pfo/0.jpg)](http://www.youtube.com/watch?v=SrS5iQV2Pfo "DeepPicar_Video")

Some other examples of the DeepPicar driving can be found at: https://photos.app.goo.gl/q40QFieD5iI9yXU42

If you wish to recreate the paper's findings, you can train one or more models using our dataset which can be found at:
https://drive.google.com/open?id=1LjIcOVH7xmbxV58lx3BClRcZ2DACfSwh

Please refer to [Embedded Platform Comparison](https://github.com/mbechtel2/DeepPicar-v2/wiki/Embedded-Platform-Evaluation) for the steps needed to run the experiments conducted in the paper.

## Hardware Configuration
DeepPicar is comprised of the following components:

* Raspberry Pi 3 Model B: $35
* New Bright 1:24 scale RC car: $10
* Playstation Eye camera: $7
* Pololu DRV8835 motor hat: $8
* External battery pack & misc.: $10

Please refer to [Parts and Assembly](https://github.com/mbechtel2/DeepPicar-v2/wiki/Parts-and-Assembly) for assembly steps,
and [Setup and Operation](https://github.com/mbechtel2/DeepPicar-v2/wiki/Setup-and-Operation) for in-depth installation
and usage instructions.

## Acknowledgement
The DeepPicar code utilizes MIT's DeepTesla (https://github.com/lexfridman/deeptesla), which provides a TensorFlow version of NVIDIA Dave-2's CNN.

NVIDIA Dave-2 (and its CNN) is described in the following paper.
https://arxiv.org/pdf/1604.07316

## Citation
The paper for DeepPicar can be found at https://arxiv.org/abs/1712.08644. It can be cited using the following BibTeX entry:

	@inproceedings{bechtel2018picar,
		title = {DeepPicar: A Low-cost Deep Neural Network-based Autonomous Car},    
		author = {Michael Garrett Bechtel and Elise McEllhiney and Minje Kim and Heechul Yun},
		booktitle = {IEEE International Conference on Embedded and Real-Time Computing Systems and Applications (RTCSA)},
		year = {2018}
	}
