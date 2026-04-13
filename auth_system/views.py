import jwt
import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Permission
from .serializers import UserSerializer

"""
ЛОГИКА ОБРАБОТКИ ЗАПРОСОВ (VIEWS)
--------------------------------
Реализация системы аутентификации и авторизации согласно ТЗ.
"""

class RegisterView(APIView):
    """Регистрация: создание пользователя с ФИО, email и паролем."""
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Вход: проверка пароля и генерация JWT-токена."""
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


        if user.is_deleted or not user.is_active:
            return Response({'detail': 'Доступ запрещен. Аккаунт удален или деактивирован'}, status=status.HTTP_403_FORBIDDEN)

        payload = {
            'id': user.id,
            'role': user.role.name if user.role else None,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'jwt': token})


class UserProfileView(APIView):
    """Обновление профиля и Мягкое удаление (ТЗ п.1)."""

    def patch(self, request):
        """Редактирование данных профиля."""
        user = User.objects.get(id=request.data.get('user_id')) # Пример упрощенной логики
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Мягкое удаление аккаунта (is_deleted=True)."""
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.is_deleted = True
            user.is_active = False # По требованию ТЗ
            user.save()
            return Response({"message": "Аккаунт успешно удален (мягкое удаление)"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    """Выход из системы (ТЗ п.1)."""
    def post(self, request):
        return Response({"message": "Вы успешно вышли из системы"}, status=status.HTTP_200_OK)


class MockOrdersView(APIView):
    """
    Вымышленный ресурс для демонстрации авторизации (ТЗ п.3).
    Проверяет права из нашей кастомной таблицы Permission.
    """
    def get(self, request):
        email = request.query_params.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "401 Unauthorized - Пользователь не определен"}, status=status.HTTP_401_UNAUTHORIZED)

        has_perm = Permission.objects.filter(
            role=user.role,
            resource_name='orders',
            can_read=True
        ).exists()

        if not has_perm:
            return Response({"error": "403 Forbidden - Нет доступа к ресурсу 'orders'"}, status=status.HTTP_403_FORBIDDEN)

        return Response([
            {"id": 1, "product": "Ноутбук", "status": "Оплачено"},
            {"id": 2, "product": "Мышь", "status": "В пути"}
        ])