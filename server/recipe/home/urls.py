from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
  path('', views.home_view, name='home'),
  path('user/<str:username>', views.profile_view, name='profile')
]