from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE_DISPLAY
