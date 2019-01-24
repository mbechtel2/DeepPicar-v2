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
The Evaluation section below details the steps needed for running the experiments conducted in the paper.

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

## Embedded Computing Platform Evaluation
The evaluations are performed using the test-model.py file. This file loads the
images from a given number of epoch ids, and feeds all images to the trained
TensorFlow model(s) defined by the 'model_load_file' value(s) from 'params.py'.
For each image, the execution time of the different control loop steps
(image capture, preprocessing, etc.) are recorded and printed while images are
being fed to the model. When all images have been processed (or the max number
of frames to be processed has been reached), the statistics (average, stardard
deviation, etc.) will be printed to the console.

By default, the platforms are tested over epoch 6 (out-video-6.avi), but
the epochs processed can be changed by altering epoch_ids in test-model.py:

	epoch_ids = [...] #Replace ... with all epochs to be processed

Also, epochs can be processed more than once (i.e. epoch_ids = [6,6] would
have the platform process epoch 6 twice).

The maximum number of frames to be processed can be increased/decreased as well by
changing:

	NFRAMES = _ #Replace _ with the total number of frames to process

### Evaluation

#### Setup

Before running evaluations, the following steps should be taken:

Create the directory where all test results will be stored:

	$ mkdir datafiles

Turn off lightdm:

	$ sudo service lightdm stop

Run the appropriate scripts for maximizing performance:

	$ ./scripts/maxperf.sh #Raspberry Pi 3 Only
	$ ./scripts/jetson-clocks.sh #NVIDIA TX2 Only

#### Evaluation Scripts

For convenience, the platforms can be fully tested by running the following
scripts:

Raspberry Pi 3 (Intel UP Board):

	$ ./scripts/model-tests.sh #Should also work on the Intel UP Board
	$ ./scripts/memguard-tests.sh
	$ ./scripts/palloc-tests.sh

NVIDIA Jetson TX2:

	$ ./scripts/tx2-tests.sh

All scripts will create a datafiles/Dataset-temp directory that will contain all of the experiment logs. It should be renamed before running another script or its contents may be partially, or completely, overwritten.

*For the multimodel tests done in the 'model-tests.sh' script, make sure that at least four trained models exist and that all 'model_load_file' values in 'params.py' are different so that the same model(s) aren't used multiple times.

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
