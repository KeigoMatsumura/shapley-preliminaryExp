# import the necessary packages
from skimage.segmentation import slic
import numpy as np
import cv2
import os

# for input image and pixel_segment_map
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

    # allocate segment number for each pixels
	for x in range(width):
		for y in range(height):
			pixel_segment_map[(x, y)] = segments[x][y]


	# get the list of pixels which belong to target segment
	tg_pixel = [k for k, v in pixel_segment_map.items() if v == tg_seg]


	# get neighbour segments 
	ans = set()
	nx = [1,1,0,-1,-1,-1,0,1]
	ny = [0,1,1,1,0,-1,-1,-1]

	for (x, y) in tg_pixel:
		for i in range(8):
			dx = x + nx[i]
			dy = y + ny[i]

			if 0 <= dx < width and 0 <= dy < height:
				segment_idx = pixel_segment_map[(dx, dy)]
				ans.add(segment_idx)
	ans = list(sorted(ans))
	return ans


def main():
	# load image
	img_path = "./Images/test_qid_tensor([[383]]).png"
	image = cv2.imread(img_path)

	# set the number of segment
	numofSegments=300

	# set the target segment which you want to get rid of the neighbour
	target_segment=int(221)

	# k is the number of how many neighbours removed
	k=int(5)
	

	# create a directory as the saving dst
	if not os.path.exists('Results'):
		os.mkdir('Results')
	if not os.path.exists('Results/neighbours'):
		os.mkdir('Results/neighbours')

	# get segments from image with applying SLIC method
	segments = calc_segments(image, numofSegments)
	neighbours = neighbour_segmentation(segments, target_segment)
	print("Target segment is " + str(target_segment))
	print("Target segment and its neighbours are... " + str(neighbours))

	# mask neighbour segments of the target segment
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	for i, neighbour in enumerate(neighbours):
		# for (i, neighbour) in enumerate(np.unique(segments)):
			mask[segments == neighbour] = 255
			mask = cv2.bitwise_not(mask)
			masked = cv2.bitwise_and(image, image, mask=mask)
			cv2.imwrite("Results/neighbours" + f"/neighbour_mask{neighbour}.png", masked)

			# show the masked region
			cv2.imshow("Mask", mask)
			cv2.imshow("Applied", masked)
			cv2.waitKey(0)

			# to re-generate the masked image, flip pixels again
			mask = cv2.bitwise_not(mask)

	# save segments
	# cv2.imwrite("Segments/" + f"/tg_seg_is_{target_segment}.png", tgseg_mask)
	cv2.imwrite("Results/" + f"/original.png", image)
	cv2.imwrite("Results/" + f"/neighbour_mask.png", mask)
	cv2.imwrite("Results/" + f"/neighbour_masked.png", masked)


if __name__ == "__main__":
	main()

