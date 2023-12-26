import numpy as np
import cv2
import os


def adjust_image_colors(img):
    in_black = np.array([0, 0, 0], dtype=np.float32)
    in_white = np.array([255, 255, 255], dtype=np.float32)
    in_gamma = np.array([1.0, 1.0, 1.0], dtype=np.float32)

    out_black = np.array([0, 0, 0], dtype=np.float32)
    out_white = np.array([255, 255, 255], dtype=np.float32)

    img = np.clip((img - in_black) / (in_white - in_black), 0, 255)
    img = (img ** (1 / in_gamma)) * (out_white - out_black) + out_black
    img = np.clip(img, 0, 255).astype(np.uint8)

    return img
