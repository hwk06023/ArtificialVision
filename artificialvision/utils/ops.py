import json
import os
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET


class NpEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy data types.
    
    Referenced by:
    https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
    Maps numpy data types to Python native types for JSON encoding.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
    

def convert_to_yolo(bbox):
    """
    Converts bounding box coordinates to YOLO format.

    Parameters:
    - bbox (list): Bounding box coordinates [x_min, y_min, x_max, y_max],
      where each coordinate is normalized to the range 0-1.

    Returns:
    - list: Bounding box in YOLO format [x_center, y_center, width, height].
    """
    x_min, y_min, x_max, y_max = bbox

    if not 0 <= x_min <= 1 or not 0 <= y_min <= 1 or not 0 <= x_max <= 1 or not 0 <= y_max <= 1:
        raise ValueError("Bbox coordinates must be normalized to the range 0-1.")

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return [x_center, y_center, width, height]


def convert_to_pascal_voc(bbox, img_width, img_height):
    """
    Converts bounding box coordinates to Pascal VOC format.

    Parameters:
    - bbox (list): Bounding box coordinates [x_min, y_min, x_max, y_max],
      where each coordinate is normalized to the range 0-1.
    - img_width (int): Width of the corresponding image.
    - img_height (int): Height of the corresponding image.

    Returns:
    - list: Bounding box in Pascal VOC format [xmin, ymin, xmax, ymax].
    """
    x_min, y_min, x_max, y_max = bbox

    if not 0 <= x_min <= 1 or not 0 <= y_min <= 1 or not 0 <= x_max <= 1 or not 0 <= y_max <= 1:
        raise ValueError("Bbox coordinates must be normalized to the range 0-1.")

    x_min = int(x_min * img_width)
    y_min = int(y_min * img_height)
    x_max = int(x_max * img_width)
    y_max = int(y_max * img_height)

    return [x_min, y_min, x_max, y_max]


def convert_to_coco(bbox, img_width, img_height):
    """
    Converts bounding box coordinates to COCO format.

    Parameters:
    - bbox (list): Bounding box coordinates [x_min, y_min, x_max, y_max],
      where each coordinate is normalized to the range 0-1.
    - img_width (int): Width of the corresponding image.
    - img_height (int): Height of the corresponding image.

    Returns:
    - list: Bounding box in COCO format [x_min, y_min, width, height].
    """
    x_min, y_min, x_max, y_max = bbox

    if not 0 <= x_min <= 1 or not 0 <= y_min <= 1 or not 0 <= x_max <= 1 or not 0 <= y_max <= 1:
        raise ValueError("Bbox coordinates must be normalized to the range 0-1.")

    x_min = int(x_min * img_width)
    y_min = int(y_min * img_height)
    x_max = int(x_max * img_width)
    y_max = int(y_max * img_height)

    width = x_max - x_min
    height = y_max - y_min

    return [x_min, y_min, width, height]


def save_yolo_format(bboxes, class_ids, file_paths, dst_dir='.'):
    """Saves bounding boxes in YOLO format to a text file.

    Parameters:
    - bboxes (3D list or ndarray): Bounding box coordinates [[[x_min, y_min, x_max, y_max],...],...],
      where each coordinate is normalized to the range 0-1.
    - class_ids (2D list or ndarray): Class ID of each bounding box.
    - file_paths (list): File paths of each image/video.
    - dst_dir (str): Destination directory to save bounding box information text files.
      The text file format is '<class_id> <x_center> <y_center> <width> <height>' per line.
    """
    annotations_dir = os.path.join(dst_dir, "Annotations_yolo")
    os.makedirs(annotations_dir, exist_ok=True)
    for bboxes_per_image, class_ids_per_image, file_path in zip(
            bboxes, class_ids, file_paths):
        img_width, img_height = Image.open(file_path).size

        file_name = f"{annotations_dir}/{file_path.split('.')[0]}.txt"
        with open(file_name, 'w') as f:
            for bbox, class_id in zip(bboxes_per_image, class_ids_per_image):
                bbox = tuple(map(float, convert_to_yolo(bbox)))
                x_center, y_center, width, height = bbox
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


def save_pascal_voc_format(bboxes, class_ids, file_paths, dst_dir='.', class_mapping=None):
    """
    Save bounding boxes in Pascal VOC format XML files within an Annotations folder.

    Parameters:
    - bboxes: 3D list or ndarray containing bounding box coordinates in the format
      [[[x_min, y_min, x_max, y_max], ...], ...] with coordinates normalized to 0-1 range.
    - class_ids: 2D list or ndarray containing class IDs for each bounding box.
    - file_paths: List of image/video file paths.
    - dst_dir: Destination directory for the Annotations folder.
    - class_mapping: Optional dictionary mapping class IDs to class names.
    """
    annotations_dir = os.path.join(dst_dir, "Annotations_pascal_voc")
    os.makedirs(annotations_dir, exist_ok=True)

    for bboxes_per_image, class_ids_per_image, file_path in zip(bboxes, class_ids, file_paths):
        img_width, img_height = Image.open(file_path).size
        base_name = os.path.basename(file_path)
        xml_file_name = os.path.splitext(base_name)[0] + '.xml'
        xml_path = os.path.join(annotations_dir, xml_file_name)

        annotation = ET.Element('annotation')
        ET.SubElement(annotation, 'folder').text = os.path.basename(dst_dir)
        ET.SubElement(annotation, 'filename').text = base_name
        size = ET.SubElement(annotation, 'size')
        ET.SubElement(size, 'width').text = str(img_width)
        ET.SubElement(size, 'height').text = str(img_height)
        ET.SubElement(size, 'depth').text = '3'  # Assuming RGB images

        for bbox, class_id in zip(bboxes_per_image, class_ids_per_image):
            object_tag = ET.SubElement(annotation, 'object')
            class_name = class_mapping.get(class_id, str(class_id)) if class_mapping else str(class_id)
            ET.SubElement(object_tag, 'name').text = class_name
            ET.SubElement(object_tag, 'pose').text = 'Unspecified'
            ET.SubElement(object_tag, 'truncated').text = '0'
            ET.SubElement(object_tag, 'difficult').text = '0'

            bndbox = ET.SubElement(object_tag, 'bndbox')
            bbox = tuple(map(int, convert_to_pascal_voc(
                bbox, img_width, img_height)))
            ET.SubElement(bndbox, 'xmin').text = str(bbox[0])
            ET.SubElement(bndbox, 'ymin').text = str(bbox[1])
            ET.SubElement(bndbox, 'xmax').text = str(bbox[2])
            ET.SubElement(bndbox, 'ymax').text = str(bbox[3])

        tree = ET.ElementTree(annotation)
        tree.write(xml_path)


def save_coco_format(bboxes, class_ids, file_paths, dst_dir='.'):
    """Saves bounding boxes in COCO format to a JSON file.

    Parameters:
    - bboxes (3D list or ndarray): Bounding box coordinates [[[x_min, y_min, x_max, y_max],...],...],
      where each coordinate is normalized to the range 0-1.
    - class_ids (2D list or ndarray): Class ID of each bounding box.
    - file_paths (list): File paths of each image/video.
    - dst_dir (str): Destination directory to save bounding box information JSON files.
      The JSON file format follows COCO annotation standards.
    """
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    annotation_id = 0

    for i, (bboxes_per_image, class_ids_per_image, file_path) in enumerate(
            zip(bboxes, class_ids, file_paths)):
        img_width, img_height = Image.open(file_path).size
        coco_format["images"].append({"id": i, "file_name": file_path})

        for bbox, class_id in zip(bboxes_per_image, class_ids_per_image):
            bbox = list(map(int, convert_to_coco(
                bbox, img_width, img_height)))
            area = bbox[2] * bbox[3]

            coco_format["annotations"].append({
                "id": annotation_id,
                "image_id": i,
                "category_id": class_id,
                "bbox": bbox,
                "area": area,
                "iscrowd": 0
            })
            annotation_id += 1

    categories = set([class_id for sublist in class_ids for class_id in sublist])
    for category_id in categories:
        coco_format["categories"].append({
            "id": category_id, "name": f"class_{category_id}"})

    with open(f"{dst_dir}/annotations.json", 'w') as f:
        json.dump(coco_format, f, indent=2, cls=NpEncoder)