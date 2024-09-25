from django.contrib.auth.models import AbstractUser
from django.db import models

<<<<<<< HEAD

=======
>>>>>>> c05b93e92ee79022cda30f15f3de326f4cfa90e7
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    