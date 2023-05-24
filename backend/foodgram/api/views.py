from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeSearchFilter
from .mixins import ListRetrieveCustomViewSet
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import(
    FavoriteSerializer, 
    IngredientSerializers, 
    RecipeCreateSerializer,
    RecipeSerializer, 
    RecipeLightSerializer, 
    ShoppingCartSerializer,
    TagSerializers
)
from recipes.models import(
    Favorite, 
    Ingredient, 
    Recipe, 
    RecipeIngredients, 
    ShoppingCart, 
    Tag
)


class TagViewSet(ListRetrieveCustomViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    
    
class IngredientViewSet(ListRetrieveCustomViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    pagination_class = None
    
    
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeSearchFilter
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        elif self.action in ['favorite', 'shopping_cart', ]:
            return RecipeLightSerializer
        return RecipeCreateSerializer
    
    def post_and_delete_recipe_to(
        self, request, model, serializer, pk
    ):
        recipe = get_object_or_404(Recipe, pk=pk)
        data = request.data.copy()
        data.update({'recipe': recipe.id})
        
        serializer = serializer(
            data=data, 
            context={'request': request}
        )
        
        if request.method == "POST":
            if model.objects.filter(user=request.user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Этот рецепт уже добавлен в список покупок(в избранное)!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data=self.get_serializer(recipe).data
            )

        elif request.method == "DELETE":
            object = model.objects.filter(
                recipe=recipe, user=request.user
            )
            if not object.exists():
                return Response(
                    {'errors': 'Этот рецепт не был добавлен в список покупок(в избранное)!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["POST", "DELETE"], detail=True)
    def favorite(self, request, **kwargs):
        pk = kwargs['pk']
        return self.post_and_delete_recipe_to(
            request,
            Favorite,
            FavoriteSerializer,
            pk
        )
        
    @action(["POST", "DELETE"], detail=True)
    def shopping_cart(self, request, **kwargs):
        pk = kwargs['pk']
        return self.post_and_delete_recipe_to(
            request,
            ShoppingCart,
            ShoppingCartSerializer,
            pk
        )
        
    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = RecipeIngredients.objects.filter(
            recipe__shopping_list__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        
        data = []
        for ingredient in ingredients:
            data.append(
                f'• {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' - {ingredient["amount"]}'
            )
            
        content = f'Список покупок:\n\n' + '\n'.join(data)
        filename = 'shopping_cart.txt'
        
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
