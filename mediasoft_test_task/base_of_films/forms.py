from django import forms
from django.forms import Textarea

from .models import Film, FilmRating, Review, FilmParticipant


class FilmFilterForm(forms.ModelForm):
    actor = forms.ModelChoiceField(queryset=FilmParticipant.objects.filter(actor=True), required=False, label='Актер')
    director = forms.ModelChoiceField(queryset=FilmParticipant.objects.filter(director=True), required=False,
                                      label='Директор')

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
