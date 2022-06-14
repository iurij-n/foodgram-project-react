from rest_framework import generics, permissions, viewsets

from recipe.models import Tag, Recipe, Ingredient
from users.models import User
from .pagination import UserListPagination
from .serializers import (TagSerializer,
                          RecipeSerializer,
                          CustomUserCreateSerializer,
                          UserDetailSerializer,
                          UserListSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer

class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = UserListPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return UserListSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = CustomUserCreateSerializer
#     permission_classes = (permissions.AllowAny,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permissions_calsses = (permissions.IsAuthenticated,)
