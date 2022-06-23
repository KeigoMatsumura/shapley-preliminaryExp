# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import argparse
import numpy as np
import cv2
import os
from PIL import Image


image = cv2.imread("./Images/test_qid_tensor([[383]]).png")

# apply SLIC and extract (approximately) the supplied number of segments
numSegments=80
segments = slic(image, n_segments = numSegments, sigma = 5)

# if not os.path.exists('SLICed_Image'):
# 	os.mkdir('SLICed_Image')
# cv2.imwrite("SLICed_Image" + f"/slic_image.png", slic_img)

# create a directory as the saving dst
if not os.path.exists('Segments'):
	os.mkdir('Segments')
if not os.path.exists('Segments/mask'):
	os.mkdir('Segments/mask')
if not os.path.exists('Segments/mask_applied'):
	os.mkdir('Segments/mask_applied')

# loop over the unique segment values
for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print ("[x] inspecting segment %d" % (i))
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == segVal] = 255
	mask = cv2.bitwise_not(mask)
	maskApplied = cv2.bitwise_and(image, image, mask=mask)


	# save segments
	cv2.imwrite("Segments/mask" + f"/segment_{i}.png", mask)
	cv2.imwrite("Segments/mask_applied" + f"/segment_{i}.png", maskApplied)

	# show the masked region
	# io.imshow("Image", image)
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", maskApplied)
	cv2.waitKey(0)
