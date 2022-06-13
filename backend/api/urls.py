from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import TagViewSet, RecipeViewSet, UserDetail, UserViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('users/', UserViewSet.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
] 