from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from passlib.hash import sha256_crypt


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    timestamp = models.DateTimeField()


    def save(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.password = sha256_crypt.encrypt(str(password))
        self.timestamp = timezone.now()


    def __str__(self):
        return self.username    



class Review(models.Model):
    restaurant_id = models.CharField(default='1', max_length=10)
    username = models.CharField(max_length=20)
    rating = models.IntegerField(
        default=0, 
        validators = [
            MinValueValidator(1), 
            MaxValueValidator(5)
        ]
    )
    description = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.username
