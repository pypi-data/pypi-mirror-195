# deal with reading and writing files

import cv2
import numpy as np
import ezexr

def read_image(image_path):
    extension = image_path.split('.')[-1]
    if extension == 'jpg' or extension == 'jpeg' or extension == 'png':
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    elif extension == 'tif' or extension == 'tiff':
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    elif extension == 'npz':
        image = np.load(image_path)['arr_0']
    elif extension == 'exr':
        image = ezexr.imread(image_path)
    else:
        raise Exception('Unknown image format.')

    return image
