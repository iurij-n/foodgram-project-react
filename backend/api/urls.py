from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TagViewSet, RecipeViewSet, UserViewSet

# Создаётся роутер
router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', UserViewSet)



urlpatterns = [
    path('', include(router.urls)),
] 