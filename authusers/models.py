from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class TypeDocument(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Roles(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone_number = models.CharField(max_length=20, blank=True)
    document_number = models.CharField(max_length=255, unique=True)
    id_type_document = models.ForeignKey(
        TypeDocument, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    id_role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    id_status = models.ForeignKey(Status, default=1, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'document_number', 'id_type_document', 'id_role', 'id_status']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
