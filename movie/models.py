from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.


CHOICES = (
    ("movie", "movie"),
    ("series", "series"),
)


class Movie(models.Model):
    id = models.AutoField
    title = models.CharField(max_length=100)
    category = models.CharField(
        max_length=10,
        choices=CHOICES,
        default="movie"
    )
    poster = models.ImageField(upload_to='posters')
    desc = models.TextField()
    director = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    cast = models.CharField(max_length=150)
    rating = models.FloatField(default=0.0)
    trailer = models.CharField(max_length=100, default='-FZ-pPFAjYY')
    date = models.DateField()

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review = models.TextField()
    rated_as = models.FloatField(default=0.0)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.review


class Contact(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=100)
    email = models.EmailField()
    query = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
