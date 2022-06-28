# import the necessary packages
from turtle import width
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from scipy.spatial import distance
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

width=256
height=256


def applySLIC(img_path, numSegments, tg_segments, k):
	# apply SLIC and extract (approximately) the supplied number of segments
	image = cv2.imread(img_path)
	segments = slic(image, n_segments = numSegments, sigma = 5)

	# cv2.imwrite("Segments/" + f"/original.png", image)
	# cv2.imwrite("Segments/" + f"/segments.png", segments)


	# loop over the unique segment values
	for (i, segVal) in enumerate(np.unique(segments)):
		# construct a mask for the segment
		print ("[x] inspecting segment %d" % (i))
		# print(segVal)
		mask = np.zeros(image.shape[:2], dtype = "uint8")
		mask[segments == segVal] = 255

		mask = cv2.bitwise_not(mask)
		maskApplied = cv2.bitwise_and(image, image, mask=mask)
		# save segments
		cv2.imwrite("Segments/mask" + f"/segment_{i}.png", mask)
		cv2.imwrite("Segments/mask_applied" + f"/segment_{i}.png", maskApplied)

		# show the masked region
		# cv2.imshow("Mask", mask)
		# cv2.imshow("Applied", maskApplied)
		# cv2.waitKey(0)

def main():
	img_path = "./Images/test_qid_tensor([[383]]).png"
	numSegments=300
	target_seg=int(55)
	k=int(5)

	# create a directory as the saving dst
	if not os.path.exists('Segments'):
		os.mkdir('Segments')
	if not os.path.exists('Segments/mask'):
		os.mkdir('Segments/mask')
	if not os.path.exists('Segments/mask_applied'):
		os.mkdir('Segments/mask_applied')

	applySLIC(img_path, numSegments, target_seg, k)

if __name__ == "__main__":
	main()