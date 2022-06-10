from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_superuser')
    search_fields = ('username',)
    empty_value_display = EMPTY_VALUE_DISPLAY
