from django.contrib.auth import get_user_model
from django.db import models

from core.models import Recipe

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_followed',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_list',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Покупки'
        verbose_name_plural = 'Покупки'
