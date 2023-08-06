import numpy as np

class basic ():
    
    def average (img):
        """Returns Average of RGB image

        Args:
            img (numpy.ndarray): RGB image (M,N,3)

        Returns:
            average (numpy.ndarray): Gray-scale image (M,N)
        """
        return (img[:,:,0] + img[:,:,1] + img[:,:,2])*(1/3)
    
    def luma (img):
        """Returns LUMA of RGB image

        Args:
            img (numpy.ndarray): RGB image (M,N,3)

        Returns:
            luma (numpy.ndarray): Gray-scale image (M,N)
        """
        return 0.299*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]
    
    
class lut ():
    
    def linear (gl, m, n):
        """Returns linearization of gray-scale image

        Args:
            gl (numpy.ndarray): Gray-scale image (M,N)
            m (scalar): Slope of linearization
            n (scalar): Bias of linearization

        Returns:
            numpy.ndarray: Linearization of gl
        """
        return m*gl + n
    
    def logistic (gl, k, gl0):
        """_summary_

        Args:
            gl (numpy.ndarray): Gray-scale image (M,N)
            k (scalar): Exponential coefficient
            gl0 (scalar): Cutoff gray level

        Returns:
            numpy.ndarray: Logistic LUT of gl
        """
        return np.max(gl) / (1 + np.exp(-k*(gl - gl0)))