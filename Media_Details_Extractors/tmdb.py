# Added just in case fetching tmdb is required
# TMDB was needed for Vidsrc.to
class TMDBExtractor:
    BASE_URL = "watchseriesx.to"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"

    def fetch_tmdb_id(self, title: str, year_releasted: str) -> str:
        return "s"