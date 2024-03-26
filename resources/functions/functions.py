import cv2
import numpy as np
from typing import List
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from math import pi, exp


class image:
    def __init__(self, path: str = None, data: np.array = None):
        if path:
            data = cv2.imread(path)
            data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
            self.originaldata = data
            # grey scale data
            self.data = cv2.cvtColor(data, cv2.COLOR_RGB2GRAY)
        else:
            self.data = data

    def plot(self) -> None:
        plt.imshow(self.data, cmap="gray", vmin=0, vmax=255)
        plt.show()


class CannyEdgeDetector:
    SOBEL_X = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    SOBEL_Y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    KERNEL_SIZE = 5
    KERNEL_SD = 1.5

    HIGH_THRESHOLD_RATIO = 0.09
    LOW_THRESHOLD_RATIO = 0.03

    WEAK_PIXEL = 25

    def __init__(self, img: image) -> None:
        self.img = img

    def __gaussianKernel__(self, n: int, s: float) -> np.array:
        """ Returns a gaussian kernel with a given dimension n and standard deviation s """
        k = (n-1) / 2
        kernel = np.zeros((n, n))
        for i in range(1, n+1):
            for j in range(1, n+1):
                kernel[i-1][j-1] = 1/(2*pi*s*s) * \
                    exp(-((i-(k+1))**2+(j-(k+1))**2)/(2*s*s))
        # Normalization Step
        kernel /= np.sum(kernel)
        return kernel

    def gaussianFilter(self) -> image:
        """ Apply the gaussian filter on the image """
        kernel = self.__gaussianKernel__(self.KERNEL_SIZE, self.KERNEL_SD)
        return image(data=convolve2d(self.img.data, kernel, mode='same'))
    
    def intensityGradient(self) -> List[np.array]:
        gaussian_filter_image = self.gaussianFilter().data
        Gx = convolve2d(gaussian_filter_image, self.SOBEL_X, mode='same')
        Gy = convolve2d(gaussian_filter_image, self.SOBEL_Y, mode='same')

        O = np.arctan2(Gy, Gx) * 180 / np.pi

        G = np.hypot(Gx, Gy)
        G = 255 * (G / G.max())

        return G, O

    def nonMaximumSuppression(self) -> image:
        """ On a given gradient direction, if current pixel is local maxima it is preserved, 0 otherwise """
        height, width = self.img.data.shape
        gradients, angle = self.intensityGradient()
        angle[angle < 0] += 180

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = gradients[i, j+1]
                    r = gradients[i, j-1]
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    q = gradients[i-1, j+1]
                    r = gradients[i+1, j-1]
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    q = gradients[i+1, j]
                    r = gradients[i-1, j]
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    q = gradients[i-1, j-1]
                    r = gradients[i+1, j+1]

                if not ((gradients[i, j] >= q) and (gradients[i, j] >= r)):
                    gradients[i, j] = 0
        return image(data=gradients)

    def doubleThreshold(self) -> image:
        supressed_img = self.nonMaximumSuppression().data

        # ThreshHolds ?
        highThreshold = np.max(supressed_img) * self.HIGH_THRESHOLD_RATIO
        lowThreshold = highThreshold * self.LOW_THRESHOLD_RATIO

        # Pixels who are above the highTreshold should be replaced with 255 as an indicator that they are strong edges
        # Pixels who are below the lowTreshold should be replaced with 0 as an indicator that they are not edges
        # Pixels who are between the high and low tresholds should be replaced with 127 as an indicator that they are weak edges

        height, width = supressed_img.shape

        for i in range(0, height):
            for j in range(0, width):
                if (supressed_img[i][j] > highThreshold):
                    supressed_img[i][j] = 255
                elif (supressed_img[i][j] < lowThreshold):
                    supressed_img[i][j] = 0
                else:
                    supressed_img[i][j] = self.WEAK_PIXEL

        return image(data=supressed_img)

    def hystheresisTracking(self) -> image:
        double_threshold_image = self.doubleThreshold().data
        height, width = double_threshold_image.shape

        for i in range(0, height):
            for j in range(0, width):
                if double_threshold_image[i][j] == 127:
                    found = False
                    for u in [i-1, i, i+1]:
                        for v in [j-1, j, j+1]:
                            if u == i and v == j:
                                continue
                            if u >= 0 and u < height and v >= 0 and v < width:
                                if (double_threshold_image[u][v] == 255):
                                    double_threshold_image[i][j] = 255
                                    found = True
                                    break
                        if found:
                            break
                    if found == False:
                        double_threshold_image[i][j] = 0
        return image(data=double_threshold_image)
