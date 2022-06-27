from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet, UserDetail,
                    CustomUserViewSet)

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet)
router.register(r'users', CustomUserViewSet, basename='customuserviewset')

urlpatterns = [
    # path('users/', UserViewSet.as_view(), name='users'),
    path('auth/', include('djoser.urls.authtoken')),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
