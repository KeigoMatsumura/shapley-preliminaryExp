# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from scipy.spatial import distance
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
# import pandas as pd




def applySLIC(img_path, numSegments, tg_segments, k):
	# apply SLIC and extract (approximately) the supplied number of segments
	image = cv2.imread(img_path)
	segments = slic(image, n_segments = numSegments, sigma = 5)

	cv2.imwrite("Segments/" + f"/original.png", image)
	cv2.imwrite("Segments/" + f"/segments.png", segments)


	# loop over the unique segment values
	for (i, segVal) in enumerate(np.unique(segments)):
		# construct a mask for the segment
		print ("[x] inspecting segment %d" % (i))
		# print(segVal)

		mask = np.zeros(image.shape[:2], dtype = "uint8")
		mask[segments == segVal] = 255
	
		if i == tg_segments:
			dist_l = []
			for seg in np.unique(segments):
				dist_l.append(calcEuclid(seg, segments[i]))
				print(len(dist_l))
				print("dist_l" + str(dist_l))
			neighbour_l = setNeighbor(dist_l, k)

			print("neighbour_l" + str(neighbour_l))

			for neighbour in neighbour_l:
				mask[segments == neighbour] = 255

			cv2.imshow("Mask", mask)
			cv2.waitKey(0)

		mask = cv2.bitwise_not(mask)
		maskApplied = cv2.bitwise_and(image, image, mask=mask)
		# save segments
		cv2.imwrite("Segments/mask" + f"/segment_{i}.png", mask)
		cv2.imwrite("Segments/mask_applied" + f"/segment_{i}.png", maskApplied)

		# show the masked region
		cv2.imshow("Mask", mask)
		cv2.imshow("Applied", maskApplied)
		cv2.waitKey(0)

def calcEuclid(segments, target_segment):
	# dist_list = []
	# cols = ['euclid', 'segment']
	# df = pd.Series(index=[], columns=cols)

	for (i, segVal) in enumerate(np.unique(segments)):
		euclid_dist = distance.euclidean(segVal, target_segment)
		# dist_list = dist_list.append(euclid_dist)
	return euclid_dist

	# df.append()

def setNeighbor(dist_list, k):
	neighbour_list = []
	dist_list.sort()
	print("dist_list:" + str(dist_list))
	# print(dist_list[:k])
	neighbour_list = dist_list[:k]
	return neighbour_list

def main():
	img_path = "./Images/test_qid_tensor([[383]]).png"
	numSegments=200
	tg_segments=int(55)
	k=int(5)

	# create a directory as the saving dst
	if not os.path.exists('Segments'):
		os.mkdir('Segments')
	if not os.path.exists('Segments/mask'):
		os.mkdir('Segments/mask')
	if not os.path.exists('Segments/mask_applied'):
		os.mkdir('Segments/mask_applied')

	applySLIC(img_path, numSegments, tg_segments, k)

if __name__ == "__main__":
	main()