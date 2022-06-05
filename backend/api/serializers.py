from rest_framework import serializers

from recipe.models import Tag, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

class RecipeSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'text', 'tag', 'cooking_time')