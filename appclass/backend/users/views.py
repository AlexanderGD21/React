from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserRegisterSerializer
from .models import User
from django.utils import timezone
from datetime import timedelta
import random


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_home(request):
    user = request.user.username
    return Response({"message": f"Bienvenido {user}, API DigitalEducas segura"})

# === Registro de usuario con envío de código ===
@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generar código de verificación
        code = str(random.randint(100000, 999999))
        user.verification_code = code
        user.is_verified = False
        user.save()

        # Enviar correo con el código
        subject = "Verificación de cuenta - DigitalEducas"
        message = f"Hola {user.username},\n\nTu código de verificación es: {code}\n\nGracias por registrarte en DigitalEducas."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response(
            {"message": "Usuario creado. Se ha enviado el código de verificación a tu correo."},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# === Verificación del código ===
@api_view(['POST'])
def verify_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    try:
        user = User.objects.get(email=email)
        if user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            user.save()
            return Response({"message": "Cuenta verificada correctamente."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Código incorrecto."}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
# === Solicitud de recuperación ===
@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        # Generar código temporal
        code = str(random.randint(100000, 999999))
        user.verification_code = code
        user.save()

        subject = "Recuperación de contraseña - DigitalEducas"
        message = (
            f"Hola {user.username},\n\n"
            f"Recibimos una solicitud para restablecer tu contraseña.\n"
            f"Tu código de recuperación es: {code}\n\n"
            f"Si no realizaste esta solicitud, ignora este mensaje."
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        return Response(
            {"message": "Se ha enviado un código de recuperación a tu correo."},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response({"error": "No existe una cuenta con ese correo."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(email=email)
        if user.verification_code != code:
            return Response({"error": "El código de verificación es incorrecto."}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar contraseña
        user.set_password(new_password)
        user.verification_code = None
        user.save()

        return Response({"message": "Tu contraseña se ha restablecido correctamente."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "No existe una cuenta con ese correo."}, status=status.HTTP_404_NOT_FOUND)
