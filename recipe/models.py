from django.db import models

class Recipe(models.Model):

    recipe_name = models.CharField()
    recipe_description = models.CharField()
    recipe_image = models.ImageField(upload_to="uploads/")
