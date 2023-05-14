from django.contrib.auth import get_user_model
from django.db import models

from core.models import Recipe

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_followed',
        verbose_name='Блогер'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.user.username} follows {self.following.username}"


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list',
        verbose_name='Повар'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return (f"{self.user.username} add to "
                f"favorite {self.recipe.name} recipe")


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Покупатель'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return (f"{self.user.username} add to "
                f"shopping cart {self.recipe.name} recipe")
