from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.admin import UserAdmin

from .models import Ingredient, IngredientsInRecipe, Recipe, Tag
from .models import TagsInRecipe, User

site.unregister(User)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'cooking_time',)
    search_fields = ('text', 'name')
    list_filter = ('author', 'name', 'tags')


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name', 'slug', 'color')


@register(TagsInRecipe)
class TagsInRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'tag')


@register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'amount', 'ingredient')


@register(User)
class CustomUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('email', 'username')
