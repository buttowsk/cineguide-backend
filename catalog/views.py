import os, requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalog.models import Movie, Catalog, CatalogMovie
from catalog.serializers import MovieSerializer, CatalogSerializer, CatalogMovieSerializer
from dotenv import load_dotenv

load_dotenv()


class CatalogView(APIView):
    def get(self, request):
        catalogs = Catalog.objects.all()
        serializer = CatalogSerializer(catalogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class CatalogDetailView(APIView):

    def verify_pk(self, pk):
        try:
            catalog = Catalog.objects.get(pk=pk)
        except Catalog.DoesNotExist:
            return Response(
                {'error': 'Catalog not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return catalog

    def get(self, request, pk):
        catalog = self.verify_pk(pk)
        serializer = CatalogSerializer(catalog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        catalog = self.verify_pk(pk)
        serializer = CatalogSerializer(catalog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        catalog = self.verify_pk(pk)
        catalog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieView(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class CatalogMovieView(APIView):
    def get(self, request):
        catalog_movies = CatalogMovie.objects.all()
        serializer = CatalogMovieSerializer(catalog_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatalogMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

