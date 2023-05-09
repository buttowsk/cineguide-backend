from rest_framework import serializers
from .models import Movie, Catalog, CatalogMovie


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    catalogs = CatalogSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CatalogMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMovie
        fields = '__all__'