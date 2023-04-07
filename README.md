# pytmdb

# TheMovieDb Python Library

A simple Python library to get movie and TV show information from TheMovieDb API. This library makes use of the requests library to make HTTP requests to the TheMovieDb API and returns data in JSON format.

## Usage

To use this library, you need to have an API key from TheMovieDb. You can get one for free from the TheMovieDb website. Once you have your API key, set it to the TMDB_API_KEY variable.

```
TMDB_API_KEY = "YOUR_API_KEY"
```

## Methode

```
tmdb = TheMovieDb()
tmdb.get_info("IMDB_ID_HERE")
tmdb.get_videos()
tmdb.get_images()
tmdb.get_ott()
tmdb.get_cast()
```

You can access the information about the movie or TV show using the attributes of the TheMovieDb instance.

```
print(tmdb.title)
print(tmdb.year)
print(tmdb.tagline)
print(tmdb.vote_average)
print(tmdb.vote_count)
print(tmdb.backdrop)
print(tmdb.poster)
print(tmdb.budget)
print(tmdb.website)
print(tmdb.language)
print(tmdb.overview)
print(tmdb.popularity)
print(tmdb.revenue)
print(tmdb.runtime)
print(tmdb.studios)
print(tmdb.genres)
print(tmdb.ott_icons)
print(tmdb.actors)
print(tmdb.directors)
print(tmdb.writers)
print(tmdb.producers)
```
