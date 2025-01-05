from django.db import models
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from efficientnet_pytorch import EfficientNet

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=200)

class Gender(models.Model):
    name = models.CharField(max_length=200)

class Results(models.Model):
    name = models.CharField(max_length=200)

class DiabetesData(models.Model):
    person_name = models.CharField(max_length=500)
    age = models.IntegerField()
    confidence_level = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    results = models.ForeignKey(Results, on_delete=models.CASCADE)

# model prediction
class DiabetesPredictor:
    def __init__(self):
        """
        Initialize the model and other required components.
        The model weights are loaded once during application runtime.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = EfficientNet.from_pretrained('efficientnet-b0')
        self.model._fc = nn.Linear(self.model._fc.in_features, 2)  # Adjust output layer for binary classification
        self.model.load_state_dict(torch.load("diabetes_model.pth", map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, image: Image.Image) -> tuple:
        """
        Predicts the class of the given image and its confidence level.

        Args:
            image (PIL.Image.Image): The input image.

        Returns:
            tuple: (predicted_class, confidence_score)
        """
        # Preprocess the image
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        # Perform inference
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted_class = torch.max(probabilities, dim=1)

        # Convert confidence tensor to a Python float
        return predicted_class.item(), confidence.item()