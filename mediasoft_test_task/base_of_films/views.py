import json
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Film, FilmActor, FilmDirector, FilmRating, Review
from .forms import FilmFilterForm, FilmRatingForm, ReviewForm
from statistics import mean
from decouple import config
import requests


class FilmListView(ListView):
    model = Film
    context_object_name = 'films'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'filter_form' not in context:
            context['filter_form'] = FilmFilterForm()
            context['actors'] = FilmActor.objects.all()
            context['directors'] = FilmDirector.objects.all()
        return context

    @staticmethod
    def post(request):
        form = FilmFilterForm(request.POST)
        if form.is_valid():
            actor = form.cleaned_data['actor']
            director = form.cleaned_data['director']
            if actor is None:
                films = Film.objects.filter(director=director)
                return render(request, 'base_of_films/film_list.html', context={'films': films, 'filter_form': form})
            if director is None:
                films = Film.objects.filter(actor=actor)
                return render(request, 'base_of_films/film_list.html', context={'films': films, 'filter_form': form})
            films = Film.objects.filter(actor=actor, director=director)
            return render(request, 'base_of_films/film_list.html', context={'films': films, 'filter_form': form})
        else:
            films = Film.objects.all()
            return render(request, 'base_of_films/film_list.html', context={'filter_form': form, 'films': films})


class FilmDetailView(DetailView):
    model = Film
    context_object_name = 'film'

    def get_rating(self):
        url = "https://imdb8.p.rapidapi.com/title/get-ratings"
        querystring = {"tconst": Film.objects.get(id=self.object.id).imdb_code}
        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': config('RAPID_API_KEY')
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return json.loads(response.text)['rating']

    @staticmethod
    def post(request, pk):
        film = Film.objects.get(id=pk)
        reviews = Review.objects.filter(film_id=pk)
        review_form = ReviewForm(request.POST)
        rating_form = FilmRatingForm(request.POST)
        if rating_form.is_valid():
            FilmRating.objects.create(user=request.user, film=film, **rating_form.cleaned_data)
            return redirect('film-detail', pk)
        elif review_form.is_valid():
            Review.objects.create(user=request.user, film=film, **review_form.cleaned_data)
            return redirect('film-detail', pk)
        return render(request, 'base_of_films/film_list.html', context={'filter_form': rating_form,
                                                                        'film': film,
                                                                        'reviews': reviews,
                                                                        'review_form': review_form
                                                                        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scores_list = [score.score for score in FilmRating.objects.filter(film_id=self.object.id)]
        context['rating_amt'] = len(scores_list)
        if context['rating_amt'] > 0:
            context['rating'] = mean(scores_list)
        context['rating_form'] = FilmRatingForm()
        context['voting_flag'] = False if len(FilmRating.objects.filter(film_id=self.object.id,
                                                                        user_id=self.request.user.id)) > 0 else True
        context['imdb_rating'] = self.get_rating()
        context['review_form'] = ReviewForm()
        context['reviews'] = Review.objects.filter(film_id=self.object.id)
        return context
