from rest_framework import serializers

from recipe.models import Tag, Recipe
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class RecipeSerializer(serializers.ModelSerializer):
    # tag = serializers.StringRelatedField(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author', 'name', 'text', 'cooking_time')