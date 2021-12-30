from django.contrib import admin
from .models import Film, FilmParticipant, FilmGenre, FilmRating


@admin.register(Film)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(FilmParticipant)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(FilmGenre)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'genre_name']


@admin.register(FilmRating)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'score', 'film', 'user']
