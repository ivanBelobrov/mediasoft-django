from django.contrib import admin
from .models import Film, FilmDirector, FilmActor, FilmGenre, FilmRating


@admin.register(Film)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(FilmActor)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']


@admin.register(FilmDirector)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']


@admin.register(FilmGenre)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'genre_name']


@admin.register(FilmRating)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'film', 'user']
