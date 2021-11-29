from rest_framework import serializers
from django.contrib.auth import get_user_model
from home.models import Recipe, Ingredient

User = get_user_model() 

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')

class RecipeSerializer(serializers.ModelSerializer):
  author = UserSerializer(many=False)

  class Meta:
    model = Recipe
    fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
  recipe = RecipeSerializer(many=False)

  class Meta:
    model = Ingredient
    fields = '__all__'