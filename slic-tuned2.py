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


img_path = './Images/test_qid_tensor([[383]]).png'
image = img_as_float(io.imread(img_path))

numSegments = 80
tg_segment = 27


# apply SLIC and extract (approximately) the supplied number of segments
segments = slic(image, n_segments = numSegments, sigma = 5)
slic_img = mark_boundaries(image, segments)

fig0, (ax0, ax1) = plt.subplots(nrows=1, ncols=2)
ax0.imshow(image)
ax1.imshow(slic_img)


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
	# print ("[x] inspecting segment %d" % (i))
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
	# io.imshow("Mask", mask)
	# cv2.imshow("Applied", fetch_segment)
	# io.imshow("Removed", remove_segment)
	# io.waitKey(0)
