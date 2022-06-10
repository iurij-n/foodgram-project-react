import email
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken

from recipe.models import Tag, Recipe
from users.models import User
from .serializers import TagSerializer, RecipeSerializer, UserSerializer, UserDetailSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        print('self.action - ', self.action, '    ', self.action == 'retrieve')
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
