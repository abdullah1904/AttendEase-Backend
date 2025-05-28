import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

class SignUpView(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    "user": serializer.data,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_201_CREATED)
            else:
                first_error = next(iter(serializer.errors.values()))[0]
                return Response({"error": first_error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Server error during user sign-up: {str(e)}", exc_info=True)
            return Response({"error": "Internal server error. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                user_data = UserSerializer(user).data
                refresh = RefreshToken.for_user(user)
                return Response({
                    "user": user_data,
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                first_error = next(iter(serializer.errors.values()))[0]
                return Response({"error": first_error}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Server error during user login: {str(e)}", exc_info=True)
            return Response({"error": "Internal server error. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)