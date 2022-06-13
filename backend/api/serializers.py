from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.shortcuts import get_object_or_404

from recipe.models import Tag, Recipe, Follow
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


# class UserDetailSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()
    
#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
    
#     def get_is_subscribed(self, obj):
#         user = self.context['request'].user
#         id = self.context['view'].kwargs['pk']
#         author = get_object_or_404(User, pk=id)
#         return Follow.objects.filter(user=user, author=author).exists()


class RecipeSerializer(serializers.ModelSerializer):
    # tag = serializers.StringRelatedField(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
    author = CustomUserCreateSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tag', 'author', 'name', 'text', 'cooking_time')


# class CurrentUserDetailSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()
    
#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')
    
#     def get_is_subscribed(self, obj):
#         # user, author = self.context['request'].user
#         # id = self.context['view'].kwargs['pk']
#         # author = get_object_or_404(User, pk=id)
#         return False
    
#     # def get_is_subscribed(self, obj):
#     #     user, author = self.context['request'].user
#     #     # id = self.context['view'].kwargs['pk']
#     #     # author = get_object_or_404(User, pk=id)
#     #     return Follow.objects.filter(user=user, author=author).exists()
