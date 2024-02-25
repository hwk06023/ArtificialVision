import torch
import numpy as np
import cv2
from torchvision import models, transforms
from PIL import Image

class Segmentation:
    def __init__(self, category=0):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.category = category
        self.model = self.load_model(category).to(self.device)
        self.model.eval()
        self.transforms = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def load_model(self, category):
        if category == 0:  # Semantic Segmentation
            return models.segmentation.fcn_resnet101(pretrained=True)
        elif category == 1:  # Instance Segmentation
            return models.detection.maskrcnn_resnet50_fpn(pretrained=True)
        elif category == 2:  # Panoptic Segmentation
            return models.segmentation.fcn_resnet101(pretrained=True)  # Example, adjust as needed
        else:
            raise ValueError("Invalid category for segmentation")

    def get_result(self, img_or_video, type=0, detail=0):
        if type == 0:  # Image
            img = Image.fromarray(cv2.cvtColor(img_or_video, cv2.COLOR_BGR2RGB))
            return self.segment_image(img, detail)
        elif type == 1:  # Video
            return self.segment_video(img_or_video, detail)
        elif type == 2:  # Webcam
            return self.segment_webcam(detail)

    def get_segment_map(self, img_or_video, type=0):
        return self.get_result(img_or_video, type, detail=1)

    def segment_image(self, img, detail):
        img_tensor = self.transforms(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(img_tensor)

        if self.category == 0:  # Semantic Segmentation
            segment_map = output['out'][0].argmax(0).byte().cpu().numpy()
        elif self.category == 1 or self.category == 2:  # Instance or Panoptic Segmentation
            # For simplicity, using semantic segmentation map
            segment_map = output['out'][0].argmax(0).byte().cpu().numpy() 

        if detail == 0:  # Overlayed Image
            return self.overlay_segment_on_image(img, segment_map)
        elif detail == 1:  # Segmentation Map
            return segment_map

    def segment_video(self, video, detail):
        while True:
            ret, frame = video.read()
            if not ret:
                break
            frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result = self.segment_image(frame, detail)
            if isinstance(result, np.ndarray):
                result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
            cv2.imshow("Segmentation Result", result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()

    def segment_webcam(self, detail):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            result = self.segment_image(frame, detail)
            if isinstance(result, np.ndarray):
                result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
            cv2.imshow("Webcam Segmentation", result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def overlay_segment_on_image(self, img, segment_map):
        # Convert PIL image to numpy array
        img = np.array(img)
        # Convert RGB to BGR
        img = img[:, :, ::-1].copy()
        # Create a mask and apply it to the image
        mask = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        mask[segment_map != 0] = [0, 255, 0]
        result = cv2.addWeighted(img, 1, mask, 0.5, 0)
        return result

