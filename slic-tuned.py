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


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = False, help = "Path to the image")
ap.add_argument("-s", "--segment", required = False, help = "Segment number to remove")
args = vars(ap.parse_args())
# load the image and convert it to a floating point data type
image = img_as_float(io.imread(args["image"]))
tg_segment = int(args["segment"])

# apply SLIC and extract (approximately) the supplied number of segments
numSegments=80
segments = slic(image, n_segments = numSegments, sigma = 5)

'''
# show the output of SLIC
fig = plt.figure("Superpixels -- %d segments" % (numSegments))
ax = fig.add_subplot(1, 1, 1)
slic_img = mark_boundaries(image, segments)

ax.imshow(slic_img)
plt.axis("off")
# show the plots
plt.show()
'''


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
if not os.path.exists('Segments/removed'):
	os.mkdir('Segments/removed')

# loop over the unique segment values
for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print ("[x] inspecting segment %d" % (i))
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == segVal] = 255
	fetch_segment = cv2.bitwise_and(image, image, mask=mask)
	remove_segment = cv2.bitwise_xor(image, image, mask=mask)

	# save segments
	cv2.imwrite("Segments/mask" + f"/segment_{i}.png", mask)
	cv2.imwrite("Segments/mask_applied" + f"/segment_{i}.png", fetch_segment)
	cv2.imwrite("Segments/removed" + f"/segment_{i}.png", remove_segment)	

	# show the masked region
	# io.imshow("Image", image)
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", fetch_segment)
	cv2.imshow("Removed", remove_segment)
	cv2.waitKey(0)

'''
for (i, segVal) in enumerate(np.unique(segments)):
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	if i == tg_segment:
		pass
	
	mask[segments == segVal] = 255

	# save image which is removed the target segment
	cv2.imwrite("Removed/mask" + f"/segment_{i}.png", mask)

'''