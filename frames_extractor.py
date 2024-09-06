import cv2
import numpy as np

class VideoFrameExtractor:
    def __init__(self, video_path, target_fpm=60):
        """
        Initializes the VideoFrameExtractor class with the path to a video file and a target frame rate per minute.

        Parameters:
        video_path (str): The path to the video file.
        target_fpm (int): The desired number of frames per minute (default is 60 FPM).
        """
        self.video_path = video_path
        self.target_fpm = target_fpm

    def extract_frames(self):
        """
        Extracts frames from the video and returns them as a list of numpy arrays.

        Returns:
        list: A list of numpy arrays representing the frames of the video.
        """
        # Create a VideoCapture object
        cap = cv2.VideoCapture(self.video_path)

        # Check if video opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
            return []

        # Get the video's FPS (frames per second) and duration
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_seconds = total_frames / fps  # Total duration in seconds
        duration_minutes = duration_seconds / 60.0  # Convert duration to minutes

        # Calculate the frame interval based on target FPM
        frames_to_process = int(self.target_fpm * duration_minutes)
        frame_interval = max(int(total_frames / frames_to_process), 1)

        # Create a list to hold the images
        images_list = []

        # Read frames from the video
        frame_counter = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Break the loop if there are no frames left

            # Process every nth frame (based on frame_interval)
            if frame_counter % frame_interval == 0:
                frame_processed = cv2.resize(frame, (384, 384))  # Resize the frame
                frame_processed = np.transpose(frame_processed, (2, 0, 1))  # Change channel order
                frame_processed = np.expand_dims(frame_processed, axis=0)  # Add batch dimension
                images_list.append(frame_processed)

            frame_counter += 1

        # Release the VideoCapture object
        cap.release()

        return images_list

# Example usage:
if __name__ == '__main__':
    video_path = 'path_to_your_video.mp4'  # Replace with your video path
    extractor = VideoFrameExtractor(video_path, target_fpm=60)
    frames = extractor.extract_frames()
    print(f"Extracted {len(frames)} frames from the video.")
