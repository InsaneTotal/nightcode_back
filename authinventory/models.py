from django.db import models


# Create your models here.

def drink_image_path(instance, filename):
    # guarda la imagen según la categoría
    return f"categories/{instance.category.name}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Drink(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='drinks'
    )
    name = models.CharField(max_length=150)
    url_img = models.ImageField(
        upload_to=drink_image_path,
        blank=True,
        null=True
    )
    # url_img = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(blank=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name
