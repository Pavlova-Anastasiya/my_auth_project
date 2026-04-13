from rest_framework import serializers
from .models import User, Role

"""
Класс UserSerializer (Сериализатор пользователя)
-----------------------------------------------
Выполняет две основные задачи:
1. Преобразует данные из базы данных в формат JSON для отправки клиенту.
2. Валидирует и подготавливает данные при создании нового пользователя.

Метод create:
Автоматически вызывается при регистрации. Выполняет шифрование пароля 
перед сохранением в базу данных для обеспечения безопасности.
"""

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fio', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Создает нового пользователя и хеширует его пароль.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

"""
Класс RoleSerializer (Сериализатор ролей)
-----------------------------------------
Выполняет функцию преобразования объектов Role в JSON. 
Используется для административных задач или отображения списка ролей в API.
"""
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'