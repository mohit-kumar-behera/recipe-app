from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

from home.models import Recipe, Ingredient

User = get_user_model()


def home_view(request):
  return render(request, 'home/home.html')


@login_required(login_url='/')
def profile_view(request, username):
  context = {'is_other_user': False, 'username': username}
  if request.user.username != username:
    context['is_other_user'] = True
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      messages.error(request, 'Requested user\'s profile doesnot exists')
      return redirect('home:home')
    except MultipleObjectsReturned:
      user = User.objects.filter(username=username).first()
    context['other_user'] = user
  return render(request, 'home/profile.html', context)


def recipe_detail_view(request, slug):
  return render(request, 'home/recipe.html')


@login_required(login_url='/')
def recipe_create_view(request):
  return render(request, 'home/recipe-form.html')


@login_required(login_url='/')
def recipe_submit_view(request):
  if request.method == 'POST':
    post_body = request.POST
    post_files = request.FILES

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