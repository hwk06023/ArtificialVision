import torch
import numpy as np
import cv2
from torchvision import models, transforms
from PIL import Image

"""
Not yet
"""


# Model loading function
def load_segmentation_model(category):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if category == 0:  # Semantic Segmentation
        model = models.segmentation.fcn_resnet101(pretrained=True)
    elif category == 1:  # Instance Segmentation
        model = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    elif category == 2:  # Panoptic Segmentation
        model = models.segmentation.fcn_resnet101(
            pretrained=True
        )  # Example, adjust as needed
    else:
        raise ValueError("Invalid category for segmentation")
    model = model.to(device)
    model.eval()
    return model, device


# Image transformation function
def get_transform():
    return transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


# Image segmentation function
def segment_image(img_or_video, category, type=0, detail=0):
    model, device = load_segmentation_model(category)
    transform = get_transform()

    if type == 0:  # Image
        img = Image.fromarray(cv2.cvtColor(img_or_video, cv2.COLOR_BGR2RGB))
        img_tensor = transform(img).unsqueeze(0).to(device)
        with torch.no_grad():
            output = model(img_tensor)

        if category in [0, 1, 2]:  # Semantic, Instance, or Panoptic Segmentation
            segment_map = output["out"][0].argmax(0).byte().cpu().numpy()

        if detail == 0:  # Overlayed Image
            return overlay_segment_on_image(img, segment_map)
        elif detail == 1:  # Segmentation Map
            return segment_map


# Function to overlay segmentation map on image
def overlay_segment_on_image(img, segment_map):
    img = np.array(img)
    img = img[:, :, ::-1].copy()  # Convert RGB to BGR
    mask = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    mask[segment_map != 0] = [0, 255, 0]
    result = cv2.addWeighted(img, 1, mask, 0.5, 0)
    return result


# Video segmentation function
def segment_video(video, category, detail):
    while True:
        ret, frame = video.read()
        if not ret:
            break
        result = segment_image(frame, category, type=0, detail=detail)
        if isinstance(result, np.ndarray):
            result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        cv2.imshow("Segmentation Result", result)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()
