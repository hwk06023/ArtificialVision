import cv2
import numpy as np

'''
Not yet
'''

'''
Updated
'''
class ObjDetection:
  def __init__(self):
    self.label_color_mapping = {} 
    self.label_name_mapping = {0: 'car', 1: 'horse', 2:'human'}
    # label_name_mapping is temporary label classes
    # Should be modified to...

def draw_bbox(self, image, bbox, label='', color=None, thickness=2):
    """Draw bounding box on an image."""
    x1, y1, x2, y2 = bbox

    # Label color mapping
    if label not in self.label_color_mapping:
        self.label_color_mapping[label] = tuple(np.random.randint(0, 255, 3).tolist())

    # Set Default
    color = self.label_color_mapping.get(label, (255, 255, 255))
    class_name = self.label_name_mapping.get(label, 'unknown')

    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    if class_name:
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness=2)

    return image
