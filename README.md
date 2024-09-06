# ImagePropertyDrift
 
This repository contains a collection of Python scripts designed to process videos, extract frame properties, calculate property drifts, and manage video downloads from YouTube. The project is structured to help in analyzing property drifts in video frames between different video sets such as training and testing datasets.

## Contents

- `frames_extractor.py`: Extracts frames from video files and returns them as a list of numpy arrays.
- `image_processor.py`: Contains utility functions to process images, such as calculating aspect ratios, brightness, and other relevant image properties.
- `pipeline_propdrift.py`: A comprehensive pipeline that extracts frames from videos, computes image properties, calculates property drifts between two sets of videos, and saves the results.
- `property_calculator.py`: Calculates various properties from image frames, such as aspect ratio, area, and different types of brightness and contrasts.
- `property_drift_calculator.py`: Computes the drift in properties between two sets of images, typically representing different conditions or times.
- `video_downloader.py`: Downloads videos from YouTube and saves them to a specified directory.
- `videonoiseadder.py`: Adds noise to videos to simulate different conditions for testing property drift.

## Setup

To set up and run the scripts, you will need Python 3.x installed along with the following libraries:
- OpenCV
- NumPy
- yt-dlp
- scikit-image
- moviepy

You can install these with pip:
```bash
pip install opencv-python numpy yt-dlp scikit-image moviepy

```

Installation
Clone the repository to get started:
```
git clone https://github.com/yourusername/yourrepositoryname.git
cd yourrepositoryname
```
Usage
Run the script by specifying the paths to your training and testing video files:
```
python pipeline_propdrift.py --train_video <path_to_train_video> --test_video <path_to_test_video>
```
Parameters

-`train_video`: Path to the training video file.

-`test_video`: Path to the testing video file.
Example:

```
python pipeline_propdrift.py --train_video /path/to/train_video.mp4 --test_video /path/to/test_video.mp4
```

To create noisy data, first create a folder named `train_data` and upload your training videos into this folder. Also, create another folder named `test_data` for the output. 

Then, execute the command below to generate noisy videos, which will be added to the `test_data` folder:
```
python videonoiseadder.py --input_dir <input_data_directory_path> --output_dir <output_data_directory_path> --frames_per_minute <no_of_frames_per_minute> --gaussian <threshold> --salt_pepper <threshold> --speckle <threshold> --poisson <threshold>

```
Example

```
python videonoiseadder.py --input_dir "train_data" --output_dir "test_data" --frames_per_minute 60 --gaussian 0.5 --salt_pepper 0.8 --speckle 0.01 --poisson 0.6
```

### Types of Noise and Their Effects:

1. **Gaussian Noise**:
   - **Effect**: Adds random variations in brightness and color intensity across the image.
   - **Drift Detection**: Likely to affect properties like **Average Brightness**, **Luminance Brightness**, **Mean Red/Green/Blue Relative Intensity**, and **RMS Contrast**.

2. **Salt & Pepper Noise**:
   - **Effect**: Randomly adds black and white pixels (salt and pepper) to the image, simulating "impulse noise."
   - **Drift Detection**: Affects **Area**, **Average Brightness**, and **RMS Contrast** by creating stark pixel differences.

3. **Speckle Noise**:
   - **Effect**: Adds multiplicative noise that causes granular variation in brightness.
   - **Drift Detection**: Could influence **Luminance Brightness**, **Average Brightness**, and **RMS Contrast**.

4. **Poisson Noise**:
   - **Effect**: Adds noise based on the Poisson distribution, which affects the brightness levels.
   - **Drift Detection**: Mainly impacts **Average Brightness**, **Luminance Brightness**, and **Color Intensities**.


