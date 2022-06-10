from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.shortcuts import get_object_or_404

from recipe.models import Tag, Recipe, Follow
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class UserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password',)



class UserDetailSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')
    
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        id = self.context['view'].kwargs['pk']
        author = get_object_or_404(User, pk=id)
        return Follow.objects.filter(user=user, author=author).exists()


class RecipeSerializer(serializers.ModelSerializer):
    # tag = serializers.StringRelatedField(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author', 'name', 'text', 'cooking_time')
