from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

def upload_path(instance, filename):
  ext = filename.split('.')[1]
  return f'recipes/{instance.title}.{ext}'


class Recipe(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  slug = models.CharField(max_length=255)
  description = models.TextField()
  image = models.ImageField(upload_to=upload_path)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    super(Recipe, self).save(*args, **kwargs)


class Ingredient(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  description = models.TextField()

  def __str__(self):
    return f'#{self.recipe.title[:10]} {self.description[:15]}'