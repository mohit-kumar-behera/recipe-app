from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
  path('', views.home_view, name='home'),
  path('user/<str:username>', views.profile_view, name='profile'),
  path('recipe/create', views.recipe_create_view, name='recipe_create'),
  path('recipe/create/submit', views.recipe_submit_view, name='recipe_submit'),
  path('recipe/<slug:slug>', views.recipe_detail_view, name='recipe_detail')
]