# imports
import requests, os
from dotenv import load_dotenv
load_dotenv()

# flask
from flask import Flask, request, render_template

# CONSTANTS
TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500/"
T_ERR_MSG = "Server took too long to respond. Try again."
E_ERR_MSG = "Something went wrong: "
V_ERR_MSG = "Reponse was not valid JSON. Try again."

def search_movies(query, page=1):
    """
    Seaches for movies using TMDB API given a <query>.

    Parameters:
        query (str): the search query / what movie is being searched
    Returns:
        array containing dictionary objects - each being a movie result
    """
    url = f"{TMDB_BASE_URL}/search/movie"

    params = {
        "query": f"{query}",
        "include_adult": False,     # default
        "language": "en-US",        # default
        "page": page                # default
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        raw_data = response.json()
    except requests.exceptions.Timeout:
        return {"results": [], "page": page, "total_pages": 0, "error": T_ERR_MSG}
    except requests.exceptions.RequestException as e:
        return {"results": [], "page": page, "total_pages": 0, "error": f"{E_ERR_MSG}{e}"}
    except ValueError:
        return {"results": [], "page": page, "total_pages": 0, "error": f"{V_ERR_MSG}"}
    
    movie_results = []
    for movie in raw_data.get("results"):
        poster_path = movie.get("poster_path")

        movie_results.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "rating": movie.get("vote_average"),
            "overview": movie.get("overview"),
            "poster_url": f"{IMG_BASE_URL}{poster_path}" if poster_path else None
        })
    
    return {
        "results": movie_results,
        "page": raw_data.get("page"),
        "total_pages": raw_data.get("total_pages"),
        "error": None
    }


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/search")
def search():
    query = request.args.get("query", "")   # by default u search for "", but is required!
    page = request.args.get("page", 1, int)
    data = search_movies(query, page)
    return render_template('results.html', **data, query=query)

if __name__ == "__main__":
    app.run(debug=True)

