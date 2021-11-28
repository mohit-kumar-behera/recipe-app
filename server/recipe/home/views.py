from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

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