from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
  path('signin/', views.signin_handler, name='signin'),
  path('signup/', views.signup_handler, name='signup'),
  path('signout/', views.signout_handler, name='signout'),

  path('test/', views.test_home, name='home')
]