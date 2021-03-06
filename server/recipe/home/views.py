from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

from home.serializers import RecipeSerializer, IngredientSerializer
from home.models import Recipe, Ingredient
from home.utils import create_response_obj

User = get_user_model()


def home_view(request):
  recipes = Recipe.objects.all()
  context = {'recipes': recipes}
  return render(request, 'home/home.html', context)


@login_required(login_url='/')
def profile_view(request, username):
  context = {'is_other_user': False, 'username': username}
  logged_in_user  = request.user
  context = {'user': logged_in_user}

  if logged_in_user.username != username:
    context['is_other_user'] = True
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      messages.error(request, 'Requested user\'s profile doesnot exists')
      return redirect('home:home')
    except MultipleObjectsReturned:
      user = User.objects.filter(username=username).first()
    context['user'] = user

  recipes_of_user = context['user'].recipe_set.all()
  context['recipes'] = recipes_of_user
  return render(request, 'home/profile.html', context)


def recipe_detail_view(request, slug):
  recipe = Recipe.objects.filter(slug=slug).first()
  ingredients = recipe.ingredient_set.all()
  if not recipe:
    messages.error(request, 'Sorry, No such recipe found')
  context = {'recipe': recipe, 'ingredients': ingredients}
  print("here", ingredients)
  return render(request, 'home/recipe.html', context)


@login_required(login_url='/')
def recipe_create_view(request):
  return render(request, 'home/recipe-form.html')


@login_required(login_url='/')
def recipe_submit_view(request):
  if request.method == 'POST':
    post_body = request.POST
    post_files = request.FILES

    if not request.FILES.get('image'):
      messages.error(request, 'Please add an Image for recipe')
      return redirect('home:recipe_create')

    try:
      recipe = Recipe.objects.create(
        author=request.user,
        title=post_body.get('title'),
        description=post_body.get('description'),
        image=post_files.get('image')
      )
    except:
      messages.error(request, 'Something went wrong while adding your recipe')
      return redirect('home:recipe_create')
    else:
      try:
        with transaction.atomic():
          for ingredient in post_body.getlist('ingredient'):
            recipe.ingredient_set.create(description=ingredient)
      except:
        messages.error(request, 'Something went wrong while adding your recipe')
        return redirect('home:recipe_create')
    messages.success(request, 'Recipe was added successfully')
    return redirect('home:profile', username=request.user.username)
  messages.error(request, 'Something went very wrong')
  return redirect('home:recipe_create')


@api_view(['GET'])
def recipe_filter_handler(request):
  recipe_filter = request.GET.get('recipe', '')
  ingredient_filter = request.GET.get('ingredients', '')
  serializer = None
  tag = None
  
  if recipe_filter:
    tag = 'recipe'
    recipe_query = Recipe.objects.filter(
      Q(title__icontains=recipe_filter) | 
      Q(description__icontains=recipe_filter)
    )
    serializer = RecipeSerializer(recipe_query, many=True)

  if ingredient_filter:
    tag = 'ingredient'
    ingredient_query = Ingredient.objects.filter(
      description__icontains=ingredient_filter
    ).distinct()
    serializer = IngredientSerializer(ingredient_query, many=True)

  if serializer:
    response_obj = create_response_obj('success', tag, serializer.data)
    return Response(response_obj, status=status.HTTP_200_OK)

  response_obj = create_response_obj('fail', None, None)
  return Response(response_obj, status=status.HTTP_404_NOT_FOUND)