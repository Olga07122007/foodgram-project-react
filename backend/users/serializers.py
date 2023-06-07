from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe
from .models import Subscription, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password',
        )


class RecipeSubscribeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(CustomUserSerializer):
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscription.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                detail='вы уже подписались на этого автора',
                code=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                detail='вы не можете подписываться на самого себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        limit = (
            self.context['request'].query_params.get('recipes_limit')
        )
        recipes = obj.recipes.all()

        if limit is not None:
            limit = int(limit)
            serializer = RecipeSubscribeSerializer(
                recipes[:limit], many=True
            )
        else:
            serializer = RecipeSubscribeSerializer(recipes, many=True)
        return serializer.data

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name',)
