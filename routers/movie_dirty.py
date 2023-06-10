from fastapi import Path, Query, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Optional, List
from pydantic import BaseModel, Field
from models.movie import Movie as MovieModel
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

# None indica q es un valor opcional
class Movie(BaseModel):
    #id: int | None = None
    id: Optional[int] = None
    title: str = Field(default='Mi Pelicula', min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi Pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 9.2,
                "category": "Accion"
            }
        }

@movie_router.get('/movies', tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/movies/{id}', tags=["Movies"], response_model=Movie)
# Path es un parametro de ruta
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    #return [item for item in movies if item['id'] == id]

    #movie = list(filter(lambda x: x['id'] == id,movies))
    #return movie if len(movie) > 0 else "No existe la pelicula"

    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': "Pelicula no encontrada"}, status_code=404)
    else:
        return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.get('/movies/', tags=["Movies"], response_model=List[Movie], status_code=200)
# fast api al detectar que se esta usando la misma ruta pero con un metodo diferente
# lo que hace es que lo toma como un endpoint diferente
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    
    #results = [movies for movies in movies if movies['category'] == category]
    #return JSONResponse(content=results, status_code=200)

    #movie = list(filter(lambda x: x['category'] == category,movies))
    #return movie if len(movie) > 0 else "No existe la pelicula"
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@movie_router.post('/movies', tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    # movies.append(movie.dict())
    return JSONResponse(content='Pelicula Registrada', status_code=201)

@movie_router.put('/movies/{id}', tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result:
        return JSONResponse(content={'message': "Pelicula no encontrada"}, status_code=404)
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content='Pelicula Actualizada', status_code=200)

@movie_router.delete('/movies/{id}', tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result:
        return JSONResponse(content={'message': "Pelicula no encontrada"}, status_code=404)

    db.delete(result)
    db.commit()
    return JSONResponse(content='Pelicula Eliminada', status_code=200)

