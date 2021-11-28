from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home_view(request):
  return render(request, 'home/home.html')


@login_required(login_url='/')
def profile_view(request, username):
  return render(request, 'home/profile.html')


def recipe_detail_view(request, slug):
  return render(request, 'home/recipe.html')