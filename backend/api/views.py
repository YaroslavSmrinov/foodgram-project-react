from io import StringIO

from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api import serializers, utils
from core.models import Tag, Ingredient, Recipe
from users.models import Favorite, Follow, ShoppingCart, User


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (utils.FoodgramCurrentUserOrAdminOrReadOnly,)
    pagination_class = utils.PageLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = utils.RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return serializers.RecipeCreateUpdateSerializer
        return serializers.RecipeRetrieveSerializer

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def perform_update(self, serializer):
        author = self.request.user
        pk = self.kwargs.get('pk')
        serializer.save(author=author, id=pk)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class SubscriptionListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return user.is_subscribed.all().select_related('following')


class SubscriptionCreateDestroyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubscriptionSerializer
    http_method_names = ['post', 'delete']

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.get_user().is_followed.all()

    def perform_create(self, serializer):
        user = self.request.user
        following = self.get_user()
        serializer.save(following=following, user=user)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        following = self.get_user()
        instance = get_object_or_404(Follow, user=user, following=following)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RecipeMinifiedSerializer
    http_method_names = ['post', 'delete']
    model = Favorite

    def get_queryset(self):
        return get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))

    def create(self, request, *args, **kwargs):
        user = self.request.user
        recipe = self.get_queryset()
        if not self.model.objects.filter(user=user, recipe=recipe).exists():
            self.model.objects.create(user=user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = self.get_queryset()
        instance = get_object_or_404(self.model, user=user, recipe=recipe)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(FavoriteViewSet):
    model = ShoppingCart


@api_view(['GET'])
@renderer_classes([utils.PlainTextRenderer])
def download_shopping_cart(request):
    user = request.user
    cart = get_list_or_404(
        ShoppingCart.objects.select_related('recipe').prefetch_related(
            'recipe__ingredients_in_recipe'
        ),
        user=user
    )
    ingredients = []
    for ingredient in cart:
        ingredients.extend(
            ingredient.recipe.ingredients_in_recipe.all()
        )
    ingredients_dict = {}
    for ingredient in ingredients:
        if ingredient.ingredient_id not in ingredients_dict:
            ingredients_dict[ingredient.ingredient_id] = 0
        ingredients_dict[ingredient.ingredient_id] += ingredient.amount
    data = StringIO()
    for ingredient_id in ingredients_dict:
        ingredient = Ingredient.objects.get(id=ingredient_id)
        text = f'{ingredient.name} ({ingredient.measurement_unit}) —'
        text += f' {ingredients_dict[ingredient_id]} \n'
        data.write(text)
    data.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="list.txt"',
    }
    return Response(data, status=status.HTTP_200_OK, headers=headers)
