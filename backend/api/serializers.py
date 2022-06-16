from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipe.models import Follow, Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password',)


class UserDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
    
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        id = self.context['view'].kwargs['pk']
        author = get_object_or_404(User, pk=id)
        return Follow.objects.filter(user=user, author=author).exists()

class UserListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        if self.context['request'].auth is None:
            return False
        user = self.context['request'].user
        author = get_object_or_404(User, pk=obj.id)
        return Follow.objects.filter(user=user, author=author).exists()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
    
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        author = get_object_or_404(User, pk=obj.id)
        return Follow.objects.filter(user=user, author=author).exists()


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    
    class Meta:
       model = Ingredient
       fields = ('id', 'name', 'measurement_unit', 'amount')
    
    def get_amount(self, obj):
        recipe_ingredient = RecipeIngredient.objects.get(ingredient__id=obj.id)
        return recipe_ingredient.amount


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserCreateSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients','name', 'text', 'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
