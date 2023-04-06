# Author: Dr. Luffy
# Date: 2023-04-06

import requests

TMDB_API_KEY = 'TMDB_API_KEY'
if not TMDB_API_KEY:
    raise ValueError('Please provide a TMDB API key as an environment variable.')

class TheMovieDb:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.img_url = "https://image.tmdb.org/t/p/original/{}"
        self.yt_trailer_url = "https://www.youtube.com/watch?v={}"
        self.tmdb_id = ''
        self.type = ''
        self.imdb_id = ''
        self.tagline = ''
        self.vote_average = ''
        self.vote_count = ''
        self.backdrop = ''
        self.poster = ''
        self.budget = ''
        self.website = ''
        self.language = ''
        self.overview = ''
        self.popularity = ''
        self.revenue = ''
        self.runtime = ''
        self.studios = ''
        self.genres = ''
        self.ott_icons = []
        self.actors = []
        self.directors = []
        self.writers = []
        self.producers = []

    def get_json(self, tmdb_id: str, tmdb_type: str, endpoint: str = '') -> dict:
        url = f"https://api.themoviedb.org/3/{tmdb_type}/{tmdb_id}{endpoint}?api_key={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_videos(self):
        data = self.get_json(self.tmdb_id, self.type, endpoint="/videos")
        res = data.get("results", [])
        self.trailer = ''
        for i in res:
            if i.get("type") == "Trailer" and i.get("site") == "YouTube":
                self.trailer = self.yt_trailer_url.format(i.get("key"))
                break

    def get_images(self):
        data = self.get_json(self.tmdb_id, self.type, endpoint="/images")
        self.backdrops = []
        self.posters = []
        try:
            posters = data["posters"]
            if len(posters) > 1:
                for i in posters:
                    self.posters.append(self.img_url.format(i.get("file_path")))
        except KeyError:
            pass
        try:
            backdrops = data["backdrops"]
            if len(backdrops) > 1:
                for i in backdrops:
                    self.backdrops.append(self.img_url.format(i.get("file_path")))
        except KeyError:
            pass

    def get_info(self):
        data = self.get_json(self.tmdb_id, self.type)
        self.tagline = data.get("tagline", "")
        self.vote_average = data.get("vote_average", "")
        self.vote_count = data.get("vote_count", "")
        self.backdrop = self.img_url.format(data.get("backdrop_path", ""))
        self.poster = self.img_url.format(data.get("poster_path", ""))
        self.budget = data.get("budget", "")
        self.website = data.get("homepage", "")
        self.language = data.get("original_language", "")
        self.overview = data.get("overview", "")
        self.popularity = data.get("popularity", "")
        self.revenue = data.get("revenue", "")
        self.runtime = data.get("runtime", "")

        # Extract production companies
        if "production_companies" in data:
            self.studios = ",".join([company["name"] for company in data["production_companies"]])
        else:
            self.studios = ""

        # Extract genres
        if "genres" in data:
            self.genres = ",".join([gen["name"] for gen in data["genres"]])
        else:
            self.genres = ""


    def get_ott(self):
        # Get the list of available streaming providers for the movie or TV show
        response = self.get_json(self.tmdb_id, self.type, endpoint="/watch/providers")
        
        # Extract the list of streaming providers and their logos
        streaming_providers = []
        results = response.get("results", [])
        for result in results:
            for provider, details in result.items():
                if provider != "link":
                    for item in details:
                        logo_path = item.get("logo_path")
                        if logo_path:
                            streaming_providers.append(self.TMDB_IMG.format(logo_path))
        
        # Store the list of streaming provider logos
        self.ott_icons = streaming_providers

    def get_cast(self):
        data = self.get_json(self.tmdb_id, self.type, endpoint="/credits")
        cast_data = data.get("cast", [])
        crew_data = data.get("crew", [])
        
        self.actors = [person["name"] for person in cast_data[:5]]
        self.directors = [person["name"] for person in crew_data if person.get("job") == "Director"]
        self.writers = [person["name"] for person in crew_data if person.get("job") == "Writer"]
        self.producers = [person["name"] for person in crew_data if person.get("job") == "Producer"]

    def get_id(self, imdb_id):
        self.tmdb_id = ""
        self.type = ""
        self.imdb_id = imdb_id

        url = f"https://api.themoviedb.org/3/find/{self.imdb_id}?api_key={self.api_key}&external_source=imdb_id"
        response = requests.get(url)
        data = response.json()

        if not data:
            return

        movie_results = data.get("movie_results", [])
        tv_results = data.get("tv_results", [])

        if movie_results:
            self.TMDB = movie_results[0]
            self.title = self.TMDB.get("title")
            self.year = self.TMDB.get("release_date")[:4]
            self.release_date = self.TMDB.get("release_date")
            self.type = "movie"
            self.tmdb_id = self.TMDB.get("id")
            return True
        elif tv_results:
            self.TMDB = tv_results[0]
            self.title = self.TMDB.get("name")
            self.year = self.TMDB.get("first_air_date")[:4]
            self.release_date = self.TMDB.get("first_air_date")
            self.type = "tv"
            self.tmdb_id = self.TMDB.get("id")
            return True
        else:
            self.TMDB = None
            return False
        
'''        
tmdb = TheMovieDb()
TMDB = tmdb.get_id("tt6723592")
if TMDB:
    tmdb.get_info()
    tmdb.get_cast()
    tmdb.get_images()
    tmdb.get_videos()

    print(tmdb.title , tmdb.year)
    print(tmdb.trailer)
    print(tmdb.directors)
    print(tmdb.actors)
    print(tmdb.posters)
'''




