from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
User = get_user_model()

def signin_handler(request):
  if request.POST:
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    authenticated_user = authenticate(request, email=email, password=password)
    if authenticated_user is None:
      print("incorrect credential")
      messages.error(request, 'Either email or password is incorrect')
      return redirect('home:home')
    
    print("allow access")
    login(request, authenticated_user)
    return redirect('home:home')


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
        print("something is wrong")
        messages.error(request, 'Account with this email already exists')
        return redirect('home:home')
      else:
        print("All went good 2")
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, 'Account creation was successful. Please login to continue')
        return redirect('home:home')
    else:
      print("something is wrong")
      messages.error(request, 'Some fields might be empty')
      return redirect('home:home')


def signout_handler(request):
  logout(request)
  return redirect('home:home')
