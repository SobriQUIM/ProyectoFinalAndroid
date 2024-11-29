from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Movie(BaseModel):
    id: int
    name: str
    description: str
    genre: str
    duration: int

class Review(BaseModel):
    rating: int
    comment: str

movies_db: Dict[int, Movie] = {}
reviews_db: Dict[int, List[Review]] = {}

@app.post("/movies/")
def add_movie(movie: Movie):
    if movie.id in movies_db:
        raise HTTPException(status_code=400, detail="La película con este ID ya existe.")
    movies_db[movie.id] = movie
    return {"message": "Película agregada exitosamente."}

@app.post("/movies/{movie_id}/reviews/")
def add_review(movie_id: int, review: Review):
    if movie_id not in movies_db:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    if not (1 <= review.rating <= 5):
        raise HTTPException(status_code=400, detail="La calificación debe estar entre 1 y 5.")
    if movie_id not in reviews_db:
        reviews_db[movie_id] = []
    reviews_db[movie_id].append(review)
    return {"message": "Reseña agregada exitosamente."}

@app.get("/movies/genre/{genre}/")
def get_movies_by_genre(genre: str):
    filtered_movies = [movie for movie in movies_db.values() if movie.genre.lower() == genre.lower()]
    if not filtered_movies:
        raise HTTPException(status_code=404, detail="No se encontraron películas para este género.")
    return filtered_movies

@app.get("/movies/{movie_id}/")
def get_movie_by_id(movie_id: int):
    movie = movies_db.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    reviews = reviews_db.get(movie_id, [])
    return {"movie": movie, "reviews": reviews}