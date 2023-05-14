from django.contrib.admin import ModelAdmin, site

from .models import Favorite, Follow, ShoppingCart


class FollowAdmin(ModelAdmin):
    list_display = ('user', 'following')


class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')


site.register(Follow, FollowAdmin)
site.register(Favorite, FavoriteAdmin)
site.register(ShoppingCart, FavoriteAdmin)
