import cv2
import numpy as np

label_color_mapping = {}
label_name_mapping = {}


def set_label_name(label_names={}):
    """Set the label names and initialize label color mapping

    Parameters
    ----------
    label_names : dict, optional
        Dictionary containing label IDs as keys and label names as values, by default {}
    """
    global label_name_mapping
    label_name_mapping = label_names

    # Label color mapping
    for label in label_name_mapping.keys():
        label_color_mapping[label] = tuple(np.random.randint(1, 256, 3).tolist())


def add_label(
    img,
    label,
    bbox,
    size=0.5,
    thickness=2,
    draw_bg=True,
    text_bg_color=(255, 255, 255),
    text_color=(0, 0, 0),
):
    (label_width, label_height), baseline = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, size, thickness
    )

    label_bg_start = (int(bbox[0]), int(bbox[1] - label_height))
    label_bg_end = (
        int(label_bg_start[0] + label_width),
        int(label_bg_start[1] + label_height),
    )
    if draw_bg:
        cv2.rectangle(
            img,
            (int(label_bg_start[0]), int(label_bg_start[1])),
            (int(label_bg_end[0]), int(label_bg_end[1])),
            text_bg_color,
            -1,
        )
    cv2.putText(
        img,
        label,
        (int(bbox[0]), int(bbox[1]) - int(3 * size)),
        cv2.FONT_HERSHEY_SIMPLEX,
        size,
        text_color,
        thickness,
    )
    return img


def draw_bbox(image, bbox, class_list="", color=None, thickness=2):
    """Draw bounding box on an image

    Parameters
    ----------
    image : ndarray
        The actual image
    bbox : list
        A list containing x_min, y_min, width, and height of the rectangle positions
    label : str, optional
        The label associated with the bounding box, by default ''
    color : tuple, optional
        The color of the bounding box, by default None
    thickness : int, optional
        The thickness of the bounding box outline, by default 2

    Returns
    -------
    ndarray
        The image with the bounding box drawn
    """
    x, y, w, h = bbox
    x1, y1, x2, y2 = x, y, x + w, y + h

    # Set Default
    color = label_color_mapping.get(class_list, (255, 255, 255))
    class_name = label_name_mapping.get(class_list, "unknown")

    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness, cv2.LINE_AA)
    if class_name:
        add_label(
            image,
            class_name,
            [x1, y1, x2, y2],
            size=0.5,
            thickness=2,
            draw_bg=True,
            text_bg_color=color,
            text_color=(0, 0, 0),
        )

    return image


def draw_segmentation(image, segmentation, class_list="", color=None, thickness=2):
    """Draw segmentation on an image

    Parameters
    ----------
    image : ndarray
        The actual image
    segmentation : list
        List of points representing the segmentation contour
    label : str, optional
        The label associated with the segmentation, by default ''
    color : tuple, optional
        The color of the segmentation, by default None
    thickness : int, optional
        The thickness of the segmentation outline, by default 2

    Returns
    -------
    ndarray
        The image with the segmentation drawn
    """

    # Set Default
    color = label_color_mapping.get(class_list, (255, 255, 255))
    class_name = label_name_mapping.get(class_list, "unknown")

    points = np.array(segmentation).reshape((-1, 2)).astype(np.int32)
    cv2.polylines(
        image,
        [points],
        isClosed=True,
        color=color,
        thickness=thickness,
        lineType=cv2.LINE_AA,
    )

    text_position = (
        np.min(points, axis=0).flatten().tolist()
    )  # Position the label name (min x, y)
    if class_name:
        add_label(
            image,
            class_name,
            text_position,
            size=0.5,
            thickness=2,
            draw_bg=True,
            text_bg_color=color,
            text_color=(0, 0, 0),
        )

    return image
