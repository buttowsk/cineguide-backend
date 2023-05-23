from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=100)

    def __repr__(self):
        return f'Catalog: {self.name}'


class Movie(models.Model):
    backdrop = models.CharField(max_length=255, null=True)
    genres = models.JSONField(null=True)
    imdb_id = models.CharField(max_length=255, unique=True, null=True)
    original_language = models.CharField(max_length=255, null=True)
    original_title = models.CharField(max_length=255, null=True)
    overview = models.TextField(null=True)
    poster = models.CharField(max_length=255, null=True)
    release_date = models.CharField(max_length=255, null=True)
    runtime = models.IntegerField(null=True)
    tagline = models.TextField(null=True)
    title = models.CharField(max_length=255, null=True)
    vote_average = models.FloatField(null=True)
    videos = models.JSONField(null=True)
    br_certification = models.CharField(max_length=255, null=True)
    us_certification = models.CharField(max_length=255, null=True)
    colors = models.CharField(max_length=255, null=True)
    catalogs = models.ManyToManyField(Catalog, through='CatalogMovie')

    def __repr__(self):
        return f'Movie: {self.title} {self.imdb_id}'


class CatalogMovie(models.Model):
    catalogo = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    filme = models.ForeignKey(Movie, on_delete=models.CASCADE)
