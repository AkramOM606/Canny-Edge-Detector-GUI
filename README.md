# Canny Edge Detection GUI with CustomTkinter

## Description

This GUI application simplifies Canny edge detection by offering a visual interface for:

* **Image Input:** Select and load an image for edge detection. Supported image formats (JPG, PNG) will be listed.
* **Parameter Adjustment:** Fine-tune the Canny edge detection algorithm's parameters, including:
    * **Gaussian Blur:** Control the amount of Gaussian blurring applied before edge detection to reduce noise.
    * **Thresholds:** Set the lower and upper thresholds for edge detection strength.
    * **Weak Pixel:** This advanced parameter allows you to adjust the threshold for considering a weak edge during hysteresis tracking.
* **Real-time Visualization:** Observe the image processing steps within the GUI, including:
    * Input Image: The original image you selected.
    * Grayscale Conversion: Witness the conversion of the color image to grayscale.
    * Gaussian Filter: Observe the application of the Gaussian filter to reduce noise.
    * Gradient Calculation: See the calculation of image gradients to identify potential edges.
    * Non-Maximum Suppression: Follow the suppression of weak edges.
    * Double Threshold: Witness the application of two thresholds to refine detected edges.
    * Hysteresis: Observe the final step where weak edges connected to strong edges are preserved.

## Key Features

* **User-friendly GUI:** Effortless interaction with Canny edge detection parameters.
* **Interactive Image Processing:** Visualize the image processing steps for better understanding.
* **Customizable Parameters:** Fine-tune the detection process for optimal results on various images.

## Installation

**Prerequisites and Dependencies:**

* Python (assumed to be installed)
* CustomTkinter
* Pillow
* Matplotlib
* OpenCV
* NumPy
* Scipy

## Running the Application

1. Clone this repository:
```bash
git clone https://github.com/AkramOM606/Canny-Edge-Detector-GUI.git
```
2. Install the additional dependencies if not present:
```bash
pip install -r requirements.txt
```
3. Launch the application using Python
```bash
python main.py
```

## Usage

The application's GUI guides you through the image selection, parameter adjustment, and output options. Simply:

1. Adjust the Canny edge detection parameters (Gaussian blur, Thresholds, Weak Pixel) to your desired levels.
2. Click the "Input an Image" button and select the image you want to process.
3. Click the "Arrow Next Button" button to go through and visualize each step of the Canny Edge Detection Algorithm.

**Note:** You can apply a specific step as many times as you want using the left steps bar! 

## Contributing

We welcome contributions to enhance this project! Feel free to:

1. Fork the repository.
2. Create a new branch for your improvements.
3. Make your changes and commit them.
4. Open a pull request to propose your contributions.

We'll review your pull request and provide feedback promptly.

## License

This project is licensed under the MIT License: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) (see LICENSE.md for details).
