from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializers, ActivationSerializer, \
    UserSerializer, ProfileSerializer, LoginSerializer, \
    ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPassCompleteSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import IsActivePermission
from rest_framework import viewsets, permissions


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializers(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(
                "Аккаунт успешно создан, вам нужно подтвердить почту", status=201
            )


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                "Аккаунт успешно активирован", status=200
            )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response("Вы успешно вышли из своего аккаунта")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(
            raise_exception=True
        ):
            serializer.set_new_password()
            return Response('Status: 200. Пароль успешно изменён')


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Вам выслали сообщение для восстановления пароля на почту')


class ForgotPassCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPassCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно обновлён')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return User.objects.filter(email=self.request.user)
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
