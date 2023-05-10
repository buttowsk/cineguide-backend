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


class AddMovies(APIView):
    def get(self, request):
        api_key = os.getenv('TMDB_API_KEY')
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page=1'
        response = requests.get(url)
        data = response.json()
        for movie in data['results']:
            response = requests.get(
                f'http://api.themoviedb.org/3/movie/{movie["id"]}?api_key={api_key}&append_to_response=videos,release_dates')
            movie_data = response.json()
            br_certification = None
            us_certification = None
            for country in movie_data['release_dates']['results']:
                if country['iso_3166_1'] == 'BR':
                    br_certification = country['release_dates'][0]['certification']
                if country['iso_3166_1'] == 'US':
                    us_certification = country['release_dates'][0]['certification']

            youtube_key = None
            for video in movie_data['videos']['results']:
                if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                    youtube_key = video['key']

            movie = Movie(
                backdrop=movie_data['backdrop_path'],
                genres=movie_data['genres'],
                imdb_id=movie_data['imdb_id'],
                original_language=movie_data['original_language'],
                original_title=movie_data['original_title'],
                overview=movie_data['overview'],
                poster=movie_data['poster_path'],
                release_date=movie_data['release_date'],
                runtime=movie_data['runtime'],
                tagline=movie_data['tagline'],
                title=movie_data['title'],
                vote_average=movie_data['vote_average'],
                videos=youtube_key,
                br_certification=br_certification,
                us_certification=us_certification,
            )
            movie.save()

        return Response(status=status.HTTP_200_OK)
