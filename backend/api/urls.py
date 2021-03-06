from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                    TagViewSet, UserDetail)

router_v1 = DefaultRouter()

router_v1.register('users', CustomUserViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
