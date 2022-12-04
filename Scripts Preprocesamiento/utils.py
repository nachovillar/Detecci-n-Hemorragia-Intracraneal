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
from scipy import ndimage


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
def window_image(image, window_center, window_width, see_all_container):

    img_min = window_center - window_width/2

    img_max = window_center + window_width/2

    window_image = image.copy()

    if see_all_container:

        window_image[window_image < img_min] = img_min

        window_image[window_image > img_max] = img_max

    else:
        window_image[window_image < img_min] = 0

        window_image[window_image > img_max] = 0

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


def get_nonzero(im):
    a, b = im.shape

    x1 = (im - np.min(im))
    x2 = np.max(x1)

    if x2 <= 0:
        image = np.zeros([a, b])
    else:
        image = x1 / x2

    return image


def genRGB(c1, c2, c3):
    c1 = get_nonzero(c1) * 255
    c1 = np.uint8(c1)

    c2 = get_nonzero(c2) * 255
    c2 = np.uint8(c2)

    c3 = get_nonzero(c3) * 255
    c3 = np.uint8(c3)

    m, n = c1.shape

    imRGB = np.zeros([m, n, 3], dtype=np.uint8)
    imRGB[:, :, 0] = c1
    imRGB[:, :, 1] = c2
    imRGB[:, :, 2] = c3

    return imRGB

def crop_image(image):

    # Create a mask with the background pixels

    mask = image == 0

    # Find the brain area

    coords = np.array(np.nonzero(~mask))

    top_left = np.min(coords, axis=1)

    bottom_right = np.max(coords, axis=1)

    print(f'Coordenada top letf: {top_left}')
    print(f'Coordenada bottom right: {bottom_right}')

    # Remove the background

    croped_image = image[top_left[0]:bottom_right[0],

                top_left[1]:bottom_right[1]]



    return croped_image



def add_pad(image, new_height=512, new_width=512):

    height, width = image.shape



    final_image = np.zeros((new_height, new_width))



    pad_left = int((new_width - width) / 2)

    pad_top = int((new_height - height) / 2)



    # Replace the pixels with the image's pixels

    final_image[pad_top:pad_top + height, pad_left:pad_left + width] = image



    return final_image