from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
User = get_user_model()

def signin_handler(request):
  if request.POST:
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    authenticated_user = authenticate(request, email=email, password=password)
    if authenticated_user is None:
      print("incorrect credential")
      return redirect('accounts:signin')
    
    print("allow login")
    login(request, authenticated_user)
    return redirect('accounts:home')
  return render(request, 'accounts/login.html')

def signup_handler(request):
  if request.POST:
    email = request.POST.get('email')
    password = request.POST.get('password')
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')

    if email and password and first_name and last_name:
      try:
        user = User.objects.create_user(email=email, password=password)
      except:
        print("something is wrong 1")
        return redirect('accounts:signup')
      else:
        print("All went good 2")
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('accounts:signin')
    else:
      print("something is wrong 3")
      return redirect('accounts:signup')
  return render(request, 'accounts/signup.html')


def signout_handler(request):
  logout(request)
  return redirect('accounts:home')

def test_home(request):
  user = request.user
  return HttpResponse(f"Home page {user}")