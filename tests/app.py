import cv2
import sys
sys.path.append('../')
from ArtificialVision.ObjDetection import ObjDetection
from ArtificialVision.Segmentation import Segmentation

obj_detector = ObjDetection()
seg_mentation = Segmentation()

image_bbox = cv2.imread('example.jpg')
image_seg = cv2.imread('example.jpg')

# Labels
labels = [0, 0, 1, 2]

# Bounding Box
bboxes = [[200, 200, 400, 400], [50, 50, 150, 150], [300, 300, 500, 500], [100, 100, 200, 200]]
for bbox, label in zip(bboxes, labels):
    image_with_bbox = obj_detector.draw_bbox(image_bbox, bbox, label)
# show image
cv2.imshow('Image with BBox', image_with_bbox)


# Segmentations
segmentations = [
    [[200, 200], [250, 225], [300, 200], [275, 250], [300, 300], [250, 275], [200, 300], [225, 250]],  # 별 모양
    [[50, 50], [75, 65], [100, 50], [90, 70], [100, 90], [75, 80], [50, 90], [60, 70]],  # 별 모양
    [[300, 300], [350, 325], [400, 300], [375, 350], [400, 400], [350, 375], [300, 400], [325, 350]],  # 별 모양
    [[100, 100], [130, 125], [160, 100], [145, 130], [160, 160], [130, 145], [100, 160], [115, 130]]  # 별 모양
]
for segmentation, label in zip(segmentations, labels):
    image_with_seg = seg_mentation.draw_segmentation(image_seg, segmentation, label)
# show image
cv2.imshow('Image with Segmentation', image_with_seg)

# exit
cv2.waitKey(0)
cv2.destroyAllWindows()