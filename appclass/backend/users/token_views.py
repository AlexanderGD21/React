from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Verificar si el usuario está activo y verificado
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Tu cuenta está desactivada. Contacta al administrador."})
        if not user.is_verified:
            raise serializers.ValidationError({"detail": "Tu cuenta no está verificada. Revisa tu correo para activarla."})

        data['username'] = user.username
        data['email'] = user.email
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
