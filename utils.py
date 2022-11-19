import torch
from PIL import Image
import numpy as np
def scale_range(img_array):
    # if img_array.max()<=1:
    # print("scaling image")
    return img_array*255, True
    # return img_array, False
def fit_array(img_array):
    return np.moveaxis(img_array,0,-1)
def normalize_range(img_array):
    # print(img_array.min())
    # for layer in img_array:
    img_array-=img_array.min()
    img_array/=img_array.max()
    img_array, _ = scale_range(img_array)
    return img_array, True

# a = torch.zeros((3,100,100))
# a = torch.min(a,dim=0)
# print(a)