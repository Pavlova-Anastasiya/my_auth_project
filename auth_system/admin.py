from django.contrib import admin
from .models import Role, User, Permission

"""
РЕГИСТРАЦИЯ МОДЕЛЕЙ В АДМИН-ПАНЕЛИ
----------------------------------
Этот код делает наши таблицы видимыми в браузере.
Теперь я смогу вручную создавать роли и проверять пользователей.
"""

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Permission)