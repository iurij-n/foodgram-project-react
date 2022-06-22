from requests import delete
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from fpdf import FPDF
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.db.models import Avg, Count, Min, Sum
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)

from recipe.models import Favorites, RecipeIngredient, Tag, Recipe, Ingredient, ShoppingCart
from users.models import User
from .permissions import AuthorOrReadOnly
from .pagination import UserListPagination, RecipeListPagination
from .serializers import (TagSerializer,
                          RecipeSerializer,
                          CustomUserCreateSerializer,
                          AddFavoritesSerializer,
                          UserListSerializer,
                          IngredientSerializer,
                          CustomUserSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipeListPagination
    permission_classes = [AuthorOrReadOnly]
    
    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == 'POST':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            if Favorites.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': f'Рецепт \"{recipe.name}\" '
                               'уже есть в избранном у пользователя '
                               f'{user.username}'},
                    status=HTTP_400_BAD_REQUEST
                )
            Favorites.objects.create(user=user, recipe=recipe)
            serializer = AddFavoritesSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            obj = Favorites.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            return Response(
                {'errors': f'У пользователя {user.username} '
                           f'в избранном нет рецепта \"{recipe.name}\"'},
                status=HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': f'Рецепт \"{recipe.name}\" '
                               'уже есть в списке покупок у пользователя '
                               f'{user.username}'},
                    status=HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = AddFavoritesSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            obj = ShoppingCart.objects.filter(user=user, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            return Response(
                {'errors': f'У пользователя {user.username} '
                           f'в списке покупок нет рецепта \"{recipe.name}\"'},
                status=HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredient.objects.filter(
            recipe_id__cart_recipe__user=user).values_list(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(Sum('amount'))
        
        filename = 'shopping_list.txt'
        shopping_list = (
            'Список покупок:\n\n'
            # f'{dt.now().strftime(conf.DATE_TIME_FORMAT)}\n\n'
        )
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient[0].capitalize()} '
                f'({ingredient[1]}) - {ingredient[2]}\n'
            )

        response = HttpResponse(shopping_list, 
                                content_type='text.txt; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    
    
    
    
    
    
    
    
    
    
    

class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    # serializer_class = CustomUserCreateSerializer
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = UserListPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return CustomUserSerializer
        # return UserListSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = CustomUserCreateSerializer
#     permission_classes = (permissions.AllowAny,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # serializer_class = UserDetailSerializer
    permissions_calsses = (permissions.IsAuthenticated,)

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    

