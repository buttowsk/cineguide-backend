from django.urls import path
from .views import CatalogView, CatalogDetailView, MovieView, CatalogMovieView, AddMovies, ClearDb

urlpatterns = [
    path('', CatalogView.as_view()),
    path('<int:pk>/', CatalogDetailView.as_view()),
    path('movies/', MovieView.as_view()),
    path('catalog-movies/', CatalogMovieView.as_view()),
    path('add-movies/', AddMovies.as_view()),
    path('clear-db/', ClearDb.as_view()),
]