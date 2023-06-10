from typing import Optional
from pydantic import BaseModel, Field

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
