import cv2
import numpy as np

class ImageProcessor:
    """
    A class for processing images and calculating various properties such as aspect ratio, area, brightness,
    luminance brightness, RMS contrast, and color channel relative intensities.
    """

    def load(self, image_path: str):
        """
        Reads an image from the specified file path using OpenCV.

        Args:
            image_path (str): Path to the image file.

        Returns:
            numpy.ndarray: Loaded image as a NumPy array.
        """
        try:
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            print(f"Error reading image: {e}")
            return None

    def calculate_aspect_ratio(self, image):
        """
        Calculates the aspect ratio of an image.

        Args:
            image: A loaded image.

        Returns:
            float: Aspect ratio (width / height).
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        height, width, _ = image.shape
        aspect_ratio = width / height
        return aspect_ratio

    def calculate_area(self, image):
        """
        Calculates the area of an image.

        Args:
            image: A loaded image.

        Returns:
            float: The area in square pixels.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        height, width, _ = image.shape
        area = width * height
        return area

    def calculate_average_brightness(self, image):
        """
        Calculates the average pixel intensity as a measure of brightness.

        Args:
            image: A loaded image.

        Returns:
            float: The average pixel intensity.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")
        return np.mean(image.flatten())

    def calculate_luminance_brightness(self, image):
        """
        Calculates the average luminance as a measure of brightness.

        Args:
            image: A loaded image.

        Returns:
            float: The average luminance.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        image = image.astype(np.float32)
        yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        y_channel = yuv[:, :, 0]
        return np.mean(y_channel.flatten())

    def calculate_rms_contrast(self, image):
        """
        Calculates the RMS contrast of an image.

        Args:
            image: A loaded image.

        Returns:
            float: The RMS contrast.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        image = image.astype(np.float32)
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        intensity_diffs = np.square(image - np.mean(image))
        rms_contrast = np.sqrt(np.mean(intensity_diffs))

        return rms_contrast

    def calculate_mean_red_relative_intensity(self, image):
        """
        Calculates the mean red relative intensity of an image.

        Args:
            image: A loaded image.

        Returns:
            float: The mean red relative intensity.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        image = image.astype(np.float32)
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        red_channel = bgr_image[:, :, 2]
        intensity_sum = np.sum(bgr_image, axis=2)
        intensity_sum[intensity_sum == 0] = 1.0
        normalized_red = red_channel / intensity_sum
        return np.mean(normalized_red)

    def calculate_mean_green_relative_intensity(self, image):
        """
        Calculates the mean green relative intensity of an image.

        Args:
            image: A loaded image.

        Returns:
            float: The mean green relative intensity.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        image = image.astype(np.float32)
        if len(image.shape) <= 2:
            raise ValueError("Image must have color channels (e.g., RGB)")

        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        green_channel = bgr_image[:, :, 1]
        intensity_sum = np.sum(bgr_image, axis=2)
        normalized_green = green_channel / np.maximum(intensity_sum, 1.0)
        return np.mean(normalized_green)

    def calculate_mean_blue_relative_intensity(self, image):
        """
        Calculates the mean blue relative intensity of an image.

        Args:
            image: A loaded image.

        Returns:
            float: The mean blue relative intensity.
        """
        if image is None:
            raise ValueError("Error loading image. Check the image path.")

        image = image.astype(np.float32)
        if len(image.shape) <= 2:
            raise ValueError("Image must have color channels (e.g., RGB)")

        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        blue_channel = bgr_image[:, :, 0]
        intensity_sum = np.sum(bgr_image, axis=2)
        normalized_blue = blue_channel / np.maximum(intensity_sum, 1.0)
        return np.mean(normalized_blue)

if __name__ == '__main__':
    processor = ImageProcessor()
    image_path = 'path_to_your_image.jpg'  # Replace with your image path
    image = processor.load(image_path)

    if image is not None:
        print("Aspect Ratio:", processor.calculate_aspect_ratio(image))
        print("Area:", processor.calculate_area(image))
        print("Average Brightness:", processor.calculate_average_brightness(image))
        print("Luminance Brightness:", processor.calculate_luminance_brightness(image))
        print("RMS Contrast:", processor.calculate_rms_contrast(image))
        print("Mean Red Relative Intensity:", processor.calculate_mean_red_relative_intensity(image))
        print("Mean Green Relative Intensity:", processor.calculate_mean_green_relative_intensity(image))
        print("Mean Blue Relative Intensity:", processor.calculate_mean_blue_relative_intensity(image))
    else:
        print("Failed to load the image.")
