from django.db import models
from django.db.models import CASCADE


class User(models.Model):
    username = models.CharField(max_length=24, unique=True)


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=256)
    genres = models.ManyToManyField('Genre')
    authors = models.ManyToManyField(Author)
    ratings = models.ManyToManyField(User, through='UserRating')

    def __str__(self):
        return self.title


class UserRating(models.Model):
    # rating_choices =
    user = models.ForeignKey(User, on_delete=CASCADE)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    rating = models.SmallIntegerField()


class Genre(models.Model):
    name = models.CharField(max_length=128)
