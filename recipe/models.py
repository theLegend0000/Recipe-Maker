from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_name = models.CharField()
    recipe_description = models.CharField()
    recipe_image = models.ImageField(upload_to="uploads/")
