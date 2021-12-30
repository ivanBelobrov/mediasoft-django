from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Film, FilmRating, Review, FilmParticipant
from .forms import FilmFilterForm, FilmRatingForm, ReviewForm


class FilmListView(ListView):
    model = Film
    context_object_name = 'films'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'filter_form' not in context:
            context['filter_form'] = FilmFilterForm()
            context['actors'] = FilmParticipant.objects.filter(actor=True)
            context['directors'] = FilmParticipant.objects.filter(director=True)
        return context

    @staticmethod
    def post(request):
        form = FilmFilterForm(request.POST)
        films = Film.objects
        if not form.is_valid():
            return render(request, 'base_of_films/film_list.html', context={'filter_form': form, 'films': films})
        actor = form.cleaned_data['actor']
        director = form.cleaned_data['director']
        if actor:
            films = films.filter(participants=actor)
        if director:
            films = films.filter(participants=director)
        return render(request, 'base_of_films/film_list.html', context={'films': films, 'filter_form': form})


class FilmDetailView(DetailView):
    model = Film
    context_object_name = 'film'

    def post(self, request, pk):
        film = Film.objects.get(id=pk)
        reviews = Review.objects.filter(film_id=pk)

        if 'review' == request.POST.get('form'):
            review_form = ReviewForm(request.POST)
            if not review_form.is_valid():
                return render(request, 'base_of_films/film_list.html',
                              context={'filter_form': self.get_context_data().rating_form,
                                       'reviews': reviews,
                                       'review_form': review_form
                                       })
            Review.objects.create(user=request.user, film=film, **review_form.cleaned_data)
            return redirect('film-detail', pk)

        elif 'rating' == request.POST.get('form'):
            rating_form = FilmRatingForm(request.POST)
            if not rating_form.is_valid():
                return render(request, 'base_of_films/film_list.html',
                              context={'filter_form': rating_form,
                                       'reviews': reviews,
                                       'review_form': self.get_context_data().review_form
                                       })
            FilmRating.objects.create(user=request.user, film=film, **rating_form.cleaned_data)
            return redirect('film-detail', pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        FilmRating.objects.filter(film_id=self.object.id)
        context['rating_amt'] = FilmRating.objects.filter(film_id=self.object.id).count()
        if context['rating_amt'] > 0:
            context['rating'] = round(FilmRating.objects.filter(film_id=self.object.id)
                                      .aggregate(Avg('score'))['score__avg'], 1)
        context['rating_form'] = FilmRatingForm()
        context['voting_flag'] = not len(FilmRating.objects.filter(film_id=self.object.id,
                                                                   user_id=self.request.user.id))
        context['review_form'] = ReviewForm()
        context['reviews'] = Review.objects.filter(film_id=self.object.id)
        context['actors'] = FilmParticipant.objects.filter(film=self.object, actor=True)
        context['directors'] = FilmParticipant.objects.filter(film=self.object, director=True)
        return context
