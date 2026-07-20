import requests, os
from dotenv import load_dotenv
load_dotenv()

url = "https://api.themoviedb.org/3/search/movie"

params = {
    "query": "huh",
    "include_adult": False,
    "language": "en-US",
    "page": 2
}

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
}

response = requests.get(url, params=params, headers=headers)
print(response.json())