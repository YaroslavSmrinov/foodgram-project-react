from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    measurement_unit = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    slug = models.SlugField(unique=True, max_length=200)
    color = ColorField()
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        through='TagsInRecipe',
        related_name='recipes',
    )
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(300),
            MinValueValidator(1)
        ]
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientsInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Игнредиенты в рецептах'
        verbose_name_plural = 'Игнредиенты в рецептах'


class TagsInRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
