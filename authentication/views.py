from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import (generics, permissions, status)
from rest_framework.response import Response
from . serializers import (MainRegisterSerializer, CustomTokenObtainPairSerializer, LogoutSerializer)


# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MainRegisterSerializer


class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {'status': True, "status_code" : status.HTTP_200_OK, 'message': 'User logged out successfully', "data" : {} }
        except AssertionError:
            response = {'status': False, "status_code" : status.HTTP_401_UNAUTHORIZED, 'message': 'Invalid or Expired Token', "data" : {} }

        return Response(response, status=response['status_code'])