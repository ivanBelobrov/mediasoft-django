from django import forms
from django.forms import Textarea

from .models import Film, FilmRating, FilmActor, FilmDirector, Review


class FilmFilterForm(forms.ModelForm):
    actor = forms.ModelChoiceField(queryset=FilmActor.objects.all(), required=False)
    director = forms.ModelChoiceField(queryset=FilmDirector.objects.all(), required=False)

    class Meta:
        model = Film
        fields = ('actor', 'director')


class FilmRatingForm(forms.ModelForm):
    score = forms.IntegerField(help_text='Оцените фильм от 1 до 5', label='Ваша оценка')

    class Meta:
        model = FilmRating
        fields = ('score',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'rows': 5, 'cols': 40}),
        }
