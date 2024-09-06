import numpy as np
from scipy.stats import ks_2samp

class DriftCalculator:
    def __init__(self):
        # Define properties directly within the class
        self.properties = {
            'Aspect Ratio': {},
            'Area': {},
            'Average Brightness': {},
            'Luminance Brightness': {},
            'RMS Contrast': {},
            'Mean Red Relative Intensity': {},
            'Mean Green Relative Intensity': {},
            'Mean Blue Relative Intensity': {}
        }

    def convert_to_float(self, data):
        if isinstance(data, dict):
            return {k: self.convert_to_float(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_float(x) for x in data]
        elif isinstance(data, (int, float, np.number)):  # This will cover int, float, and numpy number types
            return float(data)
        else:
            return data

    def calculate_property_drift(self, test_props, train_props):
        """
        Calculates drift scores and other information for image properties.

        Args:
            train_props: A dictionary containing property values for training images.
            test_props: A dictionary containing property values for testing images.
                Keys are image filenames (without path).

        Returns:
            A dictionary containing drift information for each property:
                key: Property name (from the input dictionary)
                value: A dictionary containing:
                    'Drift Score': The Kolmogorov-Smirnov statistic.
                    'p-value': The p-value associated with the KS statistic.
                    'Mean (Train)': The mean value of the property in the training dataset.
                    'Mean (Test)': The mean value of the property in the testing dataset.
        """
        drift_info = {}
        prop_scores = []
        for prop_name in self.properties.keys():
            train_data = [train_props[img_name][prop_name] for img_name in train_props if prop_name in train_props[img_name]]
            test_data = [test_props[img_name][prop_name] for img_name in test_props if prop_name in test_props[img_name]]

            # Convert lists to NumPy arrays
            train_data = np.array(train_data)
            test_data = np.array(test_data)

            # Calculate means
            mean_train = np.mean(train_data)
            mean_test = np.mean(test_data)

            # Perform Kolmogorov-Smirnov test
            ks_statistic, p_value = ks_2samp(train_data, test_data)
            prop_scores.append(float("{:.2f}".format(ks_statistic)))

            drift_info[prop_name] = {
                'Drift Score': float("{:.2f}".format(ks_statistic)),
                'p-value': float("{:.2f}".format(p_value)),
                'Mean (Train)': float("{:.2f}".format(mean_train)),
                'Mean (Test)': float("{:.2f}".format(mean_test))
            }

        drift_info = self.convert_to_float(drift_info)
        drift_score_mean = sum(prop_scores) / len(prop_scores)  # This could be returned or used further if needed

        return drift_info

# Example usage:
if __name__ == '__main__':
    drift_calculator = DriftCalculator()
    test_props = {}  # Populate with test properties dictionary
    train_props = {}  # Populate with train properties dictionary
    drift_results = drift_calculator.calculate_property_drift(test_props, train_props)
    print(drift_results)
