# views.py
from django.http import JsonResponse
from core.permission import LoginRequiredPermission
from .predictions import SkinCancerPredictor
from PIL import Image
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserCreateSerializer, UserCreateSerializer, UserSerializer, UserUpdateSerializer
predictor = SkinCancerPredictor()

class PredictSkinCancerView(APIView):
    # permission_classes = [LoginRequiredPermission]
    def post(self, request, *args, **kwargs):
        if 'image' not in request.FILES:
            return JsonResponse({"error": "No image uploaded"}, status=400)

        img_file = request.FILES['image']
        img = Image.open(img_file).convert("RGB")
        class_label, score = predictor.predict(img)

        return JsonResponse({
            "prediction": class_label,
            "confidence_score": score
        })

class LoginView(TokenObtainPairView):
    """
    Custom login view that supports authentication via email or username.
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"message": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = authenticate(email=email, password=password)

            if user is not None:
                
              refresh = RefreshToken.for_user(user)
              user_serializer = UserSerializer(user)
              response = Response({
                  'message': 'Login successful',
                  'data': user_serializer.data,
                  'access': str(refresh.access_token),
                  'refresh': str(refresh),
              }, status=status.HTTP_200_OK)

              response.set_cookie(
              key="access_token",
              value=str(refresh.access_token),
              httponly=True,
              secure=True,  # Must be True in production
              samesite="None"  # Only use "None" when `secure=True`
              )
              return response

        except User.DoesNotExist:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class UserAllDetailView(APIView):
    permission_classes = [LoginRequiredPermission]
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserMeView(APIView):
    permission_classes = [LoginRequiredPermission]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [LoginRequiredPermission]
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)