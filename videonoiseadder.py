import cv2
import numpy as np
import os
import argparse
from moviepy.editor import VideoFileClip
from skimage.util import random_noise

class VideoNoiseAdder:
    def __init__(self, input_directory, output_directory, frames_per_minute=10):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.frames_per_minute = frames_per_minute
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def _apply_noise(self, frame, noise_types):
        noisy_frame = frame
        for noise_type, noise_intensity in noise_types.items():
            if noise_type == "gaussian":
                noisy_frame = random_noise(noisy_frame, mode='gaussian', var=noise_intensity, clip=True)
            elif noise_type == "salt_pepper":
                noisy_frame = random_noise(noisy_frame, mode='s&p', amount=noise_intensity, clip=True)
            elif noise_type == "speckle":
                noisy_frame = random_noise(noisy_frame, mode='speckle', var=noise_intensity, clip=True)
            elif noise_type == "poisson":
                noisy_frame = random_noise(noisy_frame * noise_intensity, mode='poisson', clip=True)
            else:
                raise ValueError(f"Invalid noise type: {noise_type}.")
        return (255 * noisy_frame).astype(np.uint8)

    def process_videos(self, noise_types):
        for video_file in os.listdir(self.input_directory):
            video_path = os.path.join(self.input_directory, video_file)
            if not video_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                print(f"Skipping unsupported file format: {video_file}")
                continue
            print(f"Processing video: {video_file}")
            self._process_single_video(video_path, noise_types)

    def _process_single_video(self, video_path, noise_types):
        try:
            clip = VideoFileClip(video_path)
            fps = clip.fps
            duration = clip.duration
            frame_interval = max(1, int(fps * 60 / self.frames_per_minute))
            output_frames = range(0, int(fps * duration), frame_interval)

            noise_suffix = "_".join([f"{k}_{v}" for k, v in noise_types.items()])
            video_name = os.path.basename(video_path)
            video_name_no_ext = os.path.splitext(video_name)[0]
            output_filename = f"{video_name_no_ext}_{noise_suffix}.mp4"
            output_path = os.path.join(self.output_directory, output_filename)
            
            def make_frame(t):
                frame_index = int(t * fps)
                if frame_index in output_frames:
                    frame = clip.get_frame(t)
                    return self._apply_noise(frame, noise_types)
                return clip.get_frame(t)

            output_clip = VideoFileClip(video_path, has_mask=True)
            output_clip = output_clip.set_make_frame(make_frame)
            output_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            print(f"Noised video saved to {output_path}")
        except Exception as e:
            print(f"Failed to process video {video_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Add noise to videos in a directory and output to another directory.")
    parser.add_argument('--input_dir', type=str, required=True, help='Input directory containing videos')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory for noised videos')
    parser.add_argument('--frames_per_minute', type=int, default=10, help='Number of frames per minute to process')
    parser.add_argument('--gaussian', type=float, default=0.01, help='Gaussian noise intensity')
    parser.add_argument('--salt_pepper', type=float, default=0.01, help='Salt & Pepper noise intensity')
    parser.add_argument('--speckle', type=float, default=0.01, help='Speckle noise intensity')
    parser.add_argument('--poisson', type=float, default=1.0, help='Poisson noise scaling factor')

    args = parser.parse_args()
    noise_types = {
        'gaussian': args.gaussian,
        'salt_pepper': args.salt_pepper,
        'speckle': args.speckle,
        'poisson': args.poisson
    }

    noise_adder = VideoNoiseAdder(args.input_dir, args.output_dir, args.frames_per_minute)
    noise_adder.process_videos(noise_types=noise_types)

if __name__ == "__main__":
    main()
