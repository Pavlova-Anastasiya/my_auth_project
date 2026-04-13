from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    LogoutView,
    MockOrdersView
)

"""
МАРШРУТИЗАЦИЯ API (URLS)
-----------------------
Здесь определяются все конечные точки для взаимодействия с системой.
"""

urlpatterns = [
    # Публичные эндпоинты
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Эндпоинты, требующие авторизации
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Тестовый ресурс для проверки прав (Mock-View)
    path('orders/', MockOrdersView.as_view(), name='orders_mock'),
]