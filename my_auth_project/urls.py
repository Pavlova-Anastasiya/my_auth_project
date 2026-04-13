from django.contrib import admin
from django.urls import path, include

"""
ГЛАВНЫЙ ФАЙЛ МАРШРУТОВ ПРОЕКТА
Связывает основную систему Django с нашим приложением auth_system.
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth_system.urls')),
]
