from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .constants import (MAX_AMOUNT_OF_INGREDIENT,
                        MAX_COOKING_TIME,
                        MIN_AMOUNT_OF_INGREDIENT,
                        MIN_COOKING_TIME)

User = get_user_model()


class Ingredient(models.Model):
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}({self.measurement_unit})'


class Tag(models.Model):
    slug = models.SlugField(
        unique=True,
        max_length=200,
        verbose_name='Слаг тэга'
    )
    color = ColorField(verbose_name='Цвет тэга')
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='TagsInRecipe',
        related_name='recipes',
        verbose_name='Тэг'
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True,
        verbose_name='Фотография блюда'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(MAX_COOKING_TIME),
            MinValueValidator(MIN_COOKING_TIME)
        ],
        verbose_name='Время приготовления рецепта'
    )
    text = models.TextField(
        verbose_name='Текст рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )

    class Meta:
        ordering = ['-cooking_time']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт {self.name} от автора {self.author.username}.'


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Название ингредиента'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(MAX_AMOUNT_OF_INGREDIENT),
            MinValueValidator(MIN_AMOUNT_OF_INGREDIENT)
        ],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Игнредиенты в рецептах'
        verbose_name_plural = 'Игнредиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient.name} в рецепте ' \
               f'{self.recipe.name} в количестве {self.amount}.'


class TagsInRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
        verbose_name='Тэг'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.recipe.name} содержит {self.tag.name})'
