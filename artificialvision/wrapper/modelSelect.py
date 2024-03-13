# modelInput.py

# from ArtificialVision.utils import is_valid_model

import numpy as np
import torch
from torchvision import transforms
from PIL import Image
import inspect

from torchvision.models import inception_v3
from torchvision.models import shufflenet_v2_x1_0

class modelSelect:
    # modelList - built-in으로 사용가능한 모델 리스트
    # func - built-in에 포함되거나, 커스텀으로 사용하는 전처리 모델들
    # param - 모델 학습, 동작시 필요한 파라미터들
    def __init__(self, modelList, funcs):
        modelList.append("Custom")
        self.funcs = funcs
        
        print("ArtificialVision - Select Model")
        print("Builtin Model List")
        print("--------------------------------------")
        while True:
            print("Builtin Model List")
            for i in self.modelList:
                print(i)
            print("Custom")
            print("--------------------------------------")
            userInput = input("Input Model Name: ")
            # 커스텀 모델에 맞춰야하는데
            # 지금 작성한거는 Imageclassification에 맞춰서 작성한거라
            # 커스텀에 맞춰서 클래스 인자들만으로 돌아갈 수 있도록 클래스나 함수 추가해야 할듯
            if (userInput in modelList):
                break
            else:
                print("Error : Invalid Input")


            print("The model is set to " +  userInput + " as the default mode for image classification.")
            if (userInput == "Custom"):
                # 커스텀 모델 사용 부분
                break
            else:
                # 미리 훈련된 모델 불러오기
                self.model = self.funcs[userInput](pretrained=True) # 함수의 사용에 따라 param으로 받아온 인자로 변경 해야 할 수도
                self.model.eval()
                self.model_info = userInput