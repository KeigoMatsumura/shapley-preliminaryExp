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


def calc_segments(image, seg_num):
	# apply SLIC and extract (approximately) the supplied number of segments
	segments = slic(image, n_segments = seg_num, sigma = 5)
	return segments
	

def neighbour_segmentation(segments,tg_seg):
	# initialize a map to allocate which segment belongs to which
	pixel_segment_map = dict()
	for i in range(width):
		for j in range(height):
			pixel_segment_map[(i, j)] = -1
	# print(pixel_segment_map)
	# print(len(pixel_segment_map))

    # allocate segment number for each pixels
	for x in range(width):
		for y in range(height):
			pixel_segment_map[(x, y)] = segments[x][y]
	# print(pixel_segment_map)	

	# get the list of pixels which belong to target segment
	tg_pixel = [k for k, v in pixel_segment_map.items() if v == tg_seg]
	# print(tg_pixel)
	


	# get neighbour segments 
	ans = set()
	# segment = segments[tg_seg]
	
	# print(len(segment))
	# print(segment)
	nx = [1,1,0,-1,-1,-1,0,1]
	ny = [0,1,1,1,0,-1,-1,-1]

	for (x, y) in tg_pixel:
		for i in range(8):
			dx = x + nx[i]
			dy = y + ny[i]

			if 0 <= dx < width and 0 <= dy < height:
				segment_idx = pixel_segment_map[(dx, dy)]
				ans.add(segment_idx)
	ans = list(ans)
	return ans


def main():
	# load image
	img_path = "./Images/test_qid_tensor([[383]]).png"
	image = cv2.imread(img_path)

	# set the number of segment
	numofSegments=200

	# set the target segment which you want to get rid of the neighbour
	target_segment=int(10)

	# k is the number of how many neighbours you remove
	k=int(5)
	

	# create a directory as the saving dst
	if not os.path.exists('Segments'):
		os.mkdir('Segments')
	if not os.path.exists('Segments/mask'):
		os.mkdir('Segments/mask')
	if not os.path.exists('Segments/mask_applied'):
		os.mkdir('Segments/mask_applied')

	# get segments from image with applying SLIC method
	segments = calc_segments(image, numofSegments)
	neighbours = neighbour_segmentation(segments, target_segment)

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
			cv2.imshow("Mask", mask)
			cv2.imshow("Applied", maskApplied)
			cv2.waitKey(0)

	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == neighbours] = 255
	# for neighbour in neighbours:
	# 	mask[segments == neighbour] = 255

	mask = cv2.bitwise_not(mask)
	maskApplied = cv2.bitwise_and(image, image, mask=mask)

	# show the masked region
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", maskApplied)
	cv2.waitKey(0)

if __name__ == "__main__":
	main()

