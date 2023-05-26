from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredients,
    ShoppingCart,
    Tag
)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author',
        'pub_date',
    )
    search_fields = ('name',)
    readonly_fields = ('был_добавлен_в_избранное',)
    list_filter = ('author', 'name', 'tags', 'pub_date',)
    inlines = (RecipeIngredientsInline,)

    def был_добавлен_в_избранное(self, instance):
        return instance.favorites.count()


class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'recipe']
    search_fields = ['user', 'recipe']
    list_filter = ['user', 'recipe']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredients, RecipeIngredientsAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
