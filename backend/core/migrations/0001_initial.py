# Generated by Django 3.2.18 on 2023-05-13 21:20

import json

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def load_initial_data(apps, schema_editor):
    file = open('ingredient.json', encoding='utf-8')
    decoded_file = json.load(file)
    ingredient_model = apps.get_model('core', 'Ingredient')
    ingredient_model.objects.bulk_create(
        [ingredient_model(
            name=item['name'],
            measurement_unit=item['measurement_unit']
        ) for item in decoded_file
        ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
                ('name', models.CharField(max_length=200, verbose_name='Название ингредиента')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.RunPython(load_initial_data),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Фотография блюда')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления рецепта')),
                ('text', models.TextField(verbose_name='Текст рецепта')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-cooking_time'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слаг тэга')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='Цвет тэга')),
                ('name', models.CharField(max_length=200, verbose_name='Название тэга')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TagsInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_in_recipe', to='core.recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_in_recipe', to='core.tag', verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='core.TagsInRecipe', to='core.Tag', verbose_name='Тэг'),
        ),
        migrations.CreateModel(
            name='IngredientsInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5000), django.core.validators.MinValueValidator(1)], verbose_name='Количество ингредиента')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='core.ingredient', verbose_name='Название ингредиента')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='core.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Игнредиенты в рецептах',
                'verbose_name_plural': 'Игнредиенты в рецептах',
                'ordering': ['id'],
            },
        ),
    ]
