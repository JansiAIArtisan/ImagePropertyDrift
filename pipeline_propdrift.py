import json
import argparse
from frames_extractor import VideoFrameExtractor
from property_calculator import PropertyCalculator
from property_drift_calculator import DriftCalculator

class PropertyDriftPipeline:
    def __init__(self, train_video, test_video):
        self.train_video = train_video
        self.test_video = test_video
        self.property_calculator = PropertyCalculator()
        self.drift_calculator = DriftCalculator()
    
    def extract_properties(self, video_path):
        extractor = VideoFrameExtractor(video_path)
        frames = extractor.extract_frames()
        if not frames:
            print(f"No frames extracted from {video_path}. Check if the video path is correct and the file is accessible.")
        return self.property_calculator.get_images_properties(frames)

    def calculate_drift(self):
        train_props = self.extract_properties(self.train_video)
        test_props = self.extract_properties(self.test_video)
        drift_results = self.drift_calculator.calculate_property_drift(train_props,test_props)
        return drift_results

    def save_drift_to_json(self, drift_data, output_file='property_drift_results.json'):
        with open(output_file, 'w') as file:
            json.dump(drift_data, file, indent=4)

    def run(self):
        drift_data = self.calculate_drift()
        self.save_drift_to_json(drift_data)

def main():
    parser = argparse.ArgumentParser(description="Calculate property drift between a single training and testing video.")
    parser.add_argument('--train_video', type=str, required=True, help='Path to the training video')
    parser.add_argument('--test_video', type=str, required=True, help='Path to the testing video')
    
    args = parser.parse_args()
    
    pipeline = PropertyDriftPipeline(args.train_video, args.test_video)
    pipeline.run()

if __name__ == '__main__':
    main()
