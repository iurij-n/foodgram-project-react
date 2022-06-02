from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TagViewSet

# Создаётся роутер
router = DefaultRouter()

router.register('tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
] 