from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

"""
Класс UserManager
-----------------
Специальный менеджер, который необходим для работы кастомной модели User.
Выполняет функции создания обычного пользователя и суперпользователя,
так как стандартный механизм Django рассчитан на логин через username.
"""
class UserManager(BaseUserManager):
    def create_user(self, email, fio, password=None):
        if not email:
            raise ValueError('Email является обязательным полем')
        user = self.model(
            email=self.normalize_email(email),
            fio=fio,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fio, password=None):
        user = self.create_user(email, fio, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Role(models.Model):
    """
    Класс Role (Роли)
    ----------------
    Предназначен для создания уровней доступа (например: 'Администратор', 'Пользователь').
    Выполняет функцию группировки прав, чтобы не назначать их каждому пользователю отдельно.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Название роли")

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """
    Класс User (Пользователь)
    -------------------------
    Основная модель для хранения данных о сотрудниках/клиентах.
    - fio: Хранит полное имя.
    - email: Используется как уникальный идентификатор для входа.
    - is_deleted: Реализует логику мягкого удаления.
    - role: Связывает пользователя с конкретным уровнем доступа из таблицы Role.
    """
    fio = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(unique=True, verbose_name="Email")
    is_deleted = models.BooleanField(default=False, verbose_name="Статус удаления")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, verbose_name="Роль")

    # Технические поля для работы административной панели
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio']

    def __str__(self):
        return self.email


class Permission(models.Model):
    """
    Класс Permission (Права доступа)
    -------------------------------
    Описывает конкретные разрешения для каждой роли.
    - resource_name: Указывает на объект доступа (например, 'заказы').
    - can_read: Флаг на разрешение просмотра ресурса.
    - can_write: Флаг на разрешение редактирования данных.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль")
    resource_name = models.CharField(max_length=100, verbose_name="Наименование ресурса")
    can_read = models.BooleanField(default=False, verbose_name="Доступ на чтение")
    can_write = models.BooleanField(default=False, verbose_name="Доступ на изменение")

    def __str__(self):
        return f"Права {self.role.name} на {self.resource_name}"