from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TagViewSet, RecipeViewSet, UserDetail, UserViewSet, IngredientViewSet # AddFavoriteViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, 'recipes')
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('users/', UserViewSet.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    # path('recipes/<int:pk>/favorite/', AddFavoriteViewSet.as_view(), name='add_favorite')
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
] 