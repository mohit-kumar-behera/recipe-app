from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
  path('', views.home_view, name='home'),
  path('user/<str:username>', views.profile_view, name='profile'),
  path('recipe/<slug:slug>', views.recipe_detail_view, name='recipe_detail_view')
]