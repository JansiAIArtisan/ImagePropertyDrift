import cv2
import numpy as np
from image_processor import ImageProcessor

class PropertyCalculator:
    def __init__(self):
        self.processor = ImageProcessor()  # Create an instance of ImageProcessor
        self.properties = {
            'Aspect Ratio': {
                'Function': self.processor.calculate_aspect_ratio,
            },
            'Area': {
                'Function': self.processor.calculate_area,
            },
            'Average Brightness': {
                'Function': self.processor.calculate_average_brightness,
            },
            'Luminance Brightness': {
                'Function': self.processor.calculate_luminance_brightness,
            },
            'RMS Contrast': {
                'Function': self.processor.calculate_rms_contrast,
            },
            'Mean Red Relative Intensity': {
                'Function': self.processor.calculate_mean_red_relative_intensity,
            },
            'Mean Green Relative Intensity': {
                'Function': self.processor.calculate_mean_green_relative_intensity,
            },
            'Mean Blue Relative Intensity': {
                'Function': self.processor.calculate_mean_blue_relative_intensity,
            }
        }

    def get_images_properties(self, image_list):
        """
        Calculates image property values for a list of images and returns them. Accepts either paths to images
        or already-loaded image data.

        Args:
            image_list: A list of image paths or image data.

        Returns:
            A dictionary with filenames as keys and their corresponding property values as values.
        """
        image_props = {}
        for index, image_data in enumerate(image_list):
            # Check if the input is a path and load the image, otherwise use the image data directly
            if isinstance(image_data, str):
                image_data = self.processor.load(image_data)
            if image_data is None:
                continue  # If the image failed to load or is None, skip processing

            if image_data.shape[0] == 1:
                image_data = np.squeeze(image_data, axis=0)
            image_data = image_data.transpose(1, 2, 0)

            prop_values = {}
            for prop_name, prop_info in self.properties.items():
                prop_values[prop_name] = prop_info['Function'](image_data)

            # Generate a sequential name for each image or use the filename
            image_name = f'image_{index}' if isinstance(image_data, np.ndarray) else image_data
            image_props[image_name] = prop_values

        return image_props

# Example usage:
if __name__ == '__main__':
    calculator = PropertyCalculator()
    image_list = ['path_to_your_image1.jpg', 'path_to_your_image2.jpg']  # Replace with actual paths or numpy arrays
    results = calculator.get_images_properties(image_list)
    print(results)
