from django.urls import path

from .views import FilmListView, FilmDetailView

urlpatterns = [
    path('films/', FilmListView.as_view(), name='films'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film-detail')
]

