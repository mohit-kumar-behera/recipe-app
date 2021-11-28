from django.contrib import admin
from home.models import Recipe, Ingredient


class IngredientInline(admin.StackedInline):
  model = Ingredient
  extra = 5


class RecipeAdmin(admin.ModelAdmin):
  prepopulated_fields = {
    'slug': ('title',)
  }
  inlines = [IngredientInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)