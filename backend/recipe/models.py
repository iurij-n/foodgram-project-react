from tkinter import CASCADE
from django.db import models
from django.db.models import F, Q

from .validators import validate_slug
from users.models import User


class Tag(models.Model):
    """Модель Tag: тэги рецептов."""

    name = models.CharField(
        'Тэг',
        max_length = 200,
        unique=True,
        help_text='Тэг')
    color = models.CharField(
        'Цвет тэга',
        max_length = 7,
        blank=True,
        unique=True,
        help_text='Цветовой HEX-код (например, #49B64E)')
    slug = models.SlugField(
        'Префикс',
        max_length=200,
        blank=True,
        unique=True,
        # validators=[validate_slug],
        help_text='Префикс, slug')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self): 
        return self.name


class Ingredient(models.Model):
    """Модель Ingredients: продукты."""

    name = models.CharField(
        'Название продукта',
        max_length = 200,
        help_text='Название продукта')
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length = 200,
        help_text='Единица измерения')
    
    def __str__(self): 
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    """Модель Recipe: рецепты блюд."""

    name = models.CharField(
        'Название рецепта',
        max_length = 200,
        help_text='Название рецепта')
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Автор рецепта'
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Описание рецепта'
    )
    image = models.ImageField('Картинка для рецепта',
                              upload_to='recipes_img/'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        help_text='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        'Дата и время написания обзора',
        auto_now_add=True
    )

    class Meta:
        
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self): 
        return self.name


class RecipeTag(models.Model):
    """Модель связывающая рецепт и тэги"""
    
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,        
    )


class RecipeIngredient(models.Model):
    """Модель Ingredients: ингредиенты блюда."""

    recipe_id = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        # related_name='recipe',
        # help_text='Ингредиент блюда'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        # verbose_name='Название продукта',
        on_delete=models.CASCADE,
        # related_name='ingredient',
        # help_text='Название продукта'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        help_text='Количество ингредиента'
    )

    class Meta:

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

class Favorites(models.Model):
    """Модель : избранные рецепты."""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber',
        help_text='Имя подписчика'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE,
        related_name='favourites',
        help_text='Избранный рецепт'
    )
    
    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite'),
        ]


class ShoppingCart(models.Model):
    """Модель : список покупок."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='cart_user',
        help_text='Имя пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='cart_recipe',
        help_text='Рецепт в списке покупок'
    )
    
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite'),
        ]



class Follow(models.Model):
    """Система подписок на отдельных авторов"""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Имя подписчика'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='following',
        help_text='Имя автора рецепта'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow'),
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='subscribe_to_yourself'),
        ]
