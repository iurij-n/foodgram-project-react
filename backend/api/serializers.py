from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404
from django.http import Http404
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from recipe.models import (Follow,
                          Ingredient,
                          Recipe,
                          RecipeIngredient,
                          Tag,
                          Favorites,
                          ShoppingCart)
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password',)


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
        if self.context['request'].auth is None:
            return False
        user = self.context['request'].user
        author = get_object_or_404(User, pk=obj.id)
        return Follow.objects.filter(user=user, author=author).exists()


class RecipeIngredientsSerializer(serializers.HyperlinkedModelSerializer):
    
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(source='recipeingredient_set',
                                              read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'text',
                  'cooking_time')
        read_only_fields = ('is_favorite', 'is_shopping_cart')

    def get_is_favorited(self, obj):
        if self.context['request'].auth is None:
            return False
        user = self.context['request'].user
        if Favorites.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].auth is None:
            return False
        user = self.context['request'].user
        if ShoppingCart.objects.filter(user=user, recipe=obj).exists():
            return True
        return False

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Список ингредиентов не может быть пустым'})
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_obj = get_object_or_404(Ingredient,
                                           id=ingredient['id'])
            if ingredient_obj in ingredient_list:
                raise serializers.ValidationError({
                'ingredients':
                    'Нельзя добавить один и тот же ингридиент несколько раз'
                })
            ingredient_list.append(ingredient_obj)
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients':
                        'Количество ингредиента должно быть больше 0'
                })
        data['ingredients'] = ingredients
        
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Список тэгов не может быть пустым'})
        tag_list = []
        for tag in tags:
            tag_obj = get_object_or_404(Tag, id=int(tag))
            if tag_obj in tag_list:
                raise serializers.ValidationError({
                'tags': 'Нельзя добавить один и тот же тэг несколько раз'})
            tag_list.append(tag_obj)
        data['tags'] = tags

        image = self.initial_data.get('image')
        if not image:
            raise serializers.ValidationError({
                'image': 'Нельзя добавить рецепт без картинки'})
        data['image'] = image

        return data
    
    def create(self, validated_data):
        
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        user = self.context['request'].user
        recipe = Recipe.objects.create(author=user, **validated_data)
        
        recipe.tags.set(tags)
        
        for ingredient in ingredients:
            ingredient_obj = get_object_or_404(Ingredient,
                                               id=ingredient['id'])
            RecipeIngredient.objects.get_or_create(
                recipe_id=recipe,
                ingredient=ingredient_obj,
                amount=ingredient['amount']
            )
    
        return recipe
    
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        instance.tags.clear()
        tags = self.validated_data.get('tags', instance.tags)
        instance.tags.set(tags)
        
        RecipeIngredient.objects.filter(recipe_id=instance).all().delete()
        ingredients = validated_data.get('ingredients', instance.ingredients)
        for ingredient in ingredients:
            ingredient_obj = get_object_or_404(Ingredient,
                                               id=ingredient['id'])
            RecipeIngredient.objects.create(
                recipe_id=instance,
                ingredient=ingredient_obj,
                amount=ingredient['amount']
            )
        instance.save()
        return instance

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AddFavoritesSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

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