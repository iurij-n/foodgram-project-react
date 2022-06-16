from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY

from .models import Recipe, Tag, Ingredient, RecipeIngredient, Favorites, Follow, RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'text')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY

@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe_id', 'amount', 'ingredient')
    search_fields = ('recipe_id',)
    empty_value_display = EMPTY_VALUE_DISPLAY

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY

@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    empty_value_display = EMPTY_VALUE_DISPLAY

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user',)
    empty_value_display = EMPTY_VALUE_DISPLAY

@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag', 'recipe')
    search_fields = ('tag',)
    empty_value_display = EMPTY_VALUE_DISPLAY