# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:28:22 2022

@author: Villar
"""

import random
import cv2
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np
import albumentations as A


def visualize(image):
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()


def plot_examples(images, bboxes=None):
    fig = plt.figure(figsize=(15, 15))
    columns = 4
    rows = 5

    for i in range(1, len(images)):
        if bboxes is not None:
            img = visualize_bbox(images[i - 1], bboxes[i - 1], class_name="Elon")
        else:
            img = images[i-1]
        fig.add_subplot(rows, columns, i)
        plt.imshow(img)
    plt.show()


# From https://albumentations.ai/docs/examples/example_bboxes/
def visualize_bbox(img, bbox, class_name, color=(255, 0, 0), thickness=5):
    """Visualizes a single bounding box on the image"""
    x_min, y_min, x_max, y_max = map(int, bbox)
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, thickness)
    return img

#**************************************************************************************************************************************
# ****************************************** FUNCIONES PARA PREPROCESAMIENTO **********************************************************
#**************************************************************************************************************************************

# El primer paso del preprocesamiento, es pasar la imagen original al estándar en unidades HOUNSFIELD,
# ya que las DICOM pueden venir de distintas unidades médicas.
def transform_to_hu(medical_image, image):
    intercept = medical_image.RescaleIntercept

    slope = medical_image.RescaleSlope

    hu_image = image * slope + intercept

    return hu_image

# Luego de tener la imágen en unidades, hay que hacer un windowing para ver la imágenes en una escala de grises específica para ver el cerebro
def window_image(image, window_center, window_width):

    img_min = window_center - window_width // 2

    img_max = window_center + window_width // 2

    window_image = image.copy()

    window_image[window_image < img_min] = img_min

    window_image[window_image > img_max] = img_max

    return window_image


#
def resample(image, image_thickness, pixel_spacing):
    x_pixel = float(pixel_spacing[0])

    y_pixel = float(pixel_spacing[1])

    size = np.array([x_pixel, y_pixel, float(image_thickness)])

    image_shape = np.array([image.shape[0], image.shape[1], 1])

    new_shape = image_shape * size

    new_shape = np.round(new_shape)

    resize_factor = new_shape / image_shape

    resampled_image = ndimage.interpolation.zoom(np.expand_dims(image, axis=2), resize_factor)

    return resampled_image
