from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime


def film_directory_path(instance, filename):
    return f'img/{instance.imdb_code}/{filename}'


class Film(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название фильма')
    year = models.IntegerField(null=True, default=None, validators=[MinValueValidator(1885),
                                                                    MaxValueValidator(datetime.datetime.now().year)])
    actor = models.ManyToManyField('FilmActor', verbose_name='Актер', related_name='actors')
    director = models.ManyToManyField('FilmDirector', verbose_name='Режиссер', related_name='directors')
    genre = models.ForeignKey('FilmGenre', on_delete=models.CASCADE, verbose_name='Жанр')
    imdb_code = models.CharField(max_length=10, null=True, default=None)
    poster = models.ImageField(upload_to=film_directory_path, max_length=100, verbose_name='Изображение', null=True,
                               default=None)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, verbose_name='Текст рецензии')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)


class FilmActor(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class FilmDirector(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class FilmGenre(models.Model):
    genre_name = models.CharField(max_length=30, verbose_name='Название жанра')

    class Meta:
        ordering = ['genre_name']

    def __str__(self):
        return self.genre_name


class FilmRating(models.Model):
    score = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name='Рейтинг')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
