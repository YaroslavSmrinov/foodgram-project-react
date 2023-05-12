# Generated by Django 3.2.18 on 2023-05-12 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230513_0243'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['user'], 'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['user'], 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ['user'], 'verbose_name': 'Покупки', 'verbose_name_plural': 'Покупки'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_favorited', to='core.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_list', to=settings.AUTH_USER_MODEL, verbose_name='Повар'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_followed', to=settings.AUTH_USER_MODEL, verbose_name='Блогер'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_subscribed', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_shopping_cart', to='core.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
    ]
