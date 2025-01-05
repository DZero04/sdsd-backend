from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from PIL import Image
import io
from .models import DiabetesData, Region, Gender, Results, DiabetesPredictor
from .serializers import DiabetesDataSerializers, RegionSerializer

# Initialize the predictor (singleton-style)
predictor = DiabetesPredictor()


class DiabetesDataViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = DiabetesData.objects.all()
    serializer_class = DiabetesDataSerializers

    def list(self, request):
        queryset = DiabetesData.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def predict(self, request):
        """
        Handle image prediction with confidence level.
        Expects an uploaded image in the "file" field.
        """
        if "file" not in request.FILES:
            return Response({"error": "No file provided."}, status=400)
        
        file = request.FILES["file"]
        try:
            # Open the image and make a prediction
            image = Image.open(io.BytesIO(file.read())).convert("RGB")
            predicted_class, confidence = predictor.predict(image)

            return Response({
                "class": predicted_class,
                "confidence": round(confidence * 100, 2)  # Convert to percentage
            }, status=200)
        except Exception as e:
            return Response({"error": f"Failed to process the image. {str(e)}"}, status=500)


class RegionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def list(self, request):
        queryset = Region.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
