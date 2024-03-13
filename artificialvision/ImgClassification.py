# ImgClassification.py

import numpy as np
import torch
import inspect
from torchvision import transforms
from PIL import Image
from wrapper import modelSelect
from torchvision.models import resnet50
from torchvision.models import inception_v3
from torchvision.models import shufflenet_v2_x1_0
# from ArtificialVision.utils import is_valid_model


class ImgClassification():
    def __init__(self,
                 image_path = "",
                 model_size={"EfficientNetB3": [300], "ResNet50": [256],
                            "InceptionV3": [299], "VGG16": [256]},
                 model_list=["EfficientNetB3", "InceptionV3", "ResNet50"],
                 models={"EfficientNetB3": shufflenet_v2_x1_0,
                         "InceptionV3": inception_v3, "ResNet50": resnet50}):
        self.model_size = model_size
        self.modelList = model_list
        self.models = models
        self.imagePath = image_path

    def get_result(self):
        selected_model = modelSelect.modelSelect(self.modelList, self.model)
        preprocess = transforms.Compose([
            transforms.Resize(self.model_size[selected_model.model_info][0]),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

        if selected_model.model_info != "Custom":
            image = Image.open(self.image_path).convert('RGB')

            # 이미지 전처리 및 배치 차원 추가
            input_tensor = preprocess(image)
            input_batch = input_tensor.unsqueeze(0)

            # 모델에 입력 전달하여 예측 수행
            with torch.no_grad():
                output = self.model(input_batch)

            # 클래스 확률 추출
            probabilities = torch.nn.functional.softmax(output[0], dim=0)

            # 가장 높은 확률을 갖는 클래스의 인덱스와 확률 출력
            predictions = torch.max(probabilities, 0)
            return predictions
        else:
            pass