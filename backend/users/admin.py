from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

# Убираем группы
admin.site.unregister(Group)

# Расширяем стандартную админку User, добавляя профиль
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')

# Перерегистрируем User с новой админкой
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Меняем название блока в админке
admin.site.site_header = 'ERP - Экструзионное оборудование'
admin.site.index_title = 'Управление системой'