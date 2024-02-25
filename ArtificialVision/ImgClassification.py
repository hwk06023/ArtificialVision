import torch
from torchvision import models, transforms
from torchvision.transforms.functional import to_pil_image

class ImgClassification:
    def __init__(self, model_name='resnet18', num_classes=10):
        # Load the specified pre-trained model
        self.model = getattr(models, model_name)(pretrained=True)
        
        if model_name in ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']:
            num_ftrs = self.model.fc.in_features
            self.model.fc = torch.nn.Linear(num_ftrs, num_classes)
        elif model_name in ['vgg16', 'vgg19']:
            num_ftrs = self.model.classifier[6].in_features
            self.model.classifier[6] = torch.nn.Linear(num_ftrs, num_classes)
        else:
            raise ValueError('Invalid model name')

        self.model.eval()  # Set the model to evaluation mode
        
        # Define the image transformation pipeline (may need to be adjusted per model)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),  # Common size for many models
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def get_result(self, img):
        img = to_pil_image(img)
        img = self.transform(img)
        img = img.unsqueeze(0)  # Add a batch dimension
        with torch.no_grad():
            outputs = self.model(img)
            _, predicted = torch.max(outputs, 1)
            return predicted.item()
