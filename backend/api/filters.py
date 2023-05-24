from django_filters.rest_framework import(
    ModelMultipleChoiceFilter,
    FilterSet, 
    filters
)

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientSearchFilter(FilterSet):
    name = filters.CharFilter(
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name']
        
        
class RecipeSearchFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    
    is_favorited = filters.BooleanFilter(
        method='is_favorited_filter'
    )
    
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter'
    )
    
    name = filters.CharFilter()
    
    author = ModelMultipleChoiceFilter(
        field_name='author__id',
        to_field_name='username',
        queryset=User.objects.all()
    )
    
    def is_favorited_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset
        
    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset
    
    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'name')


