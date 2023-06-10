from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router


# create FastApi instance
app = FastAPI()
app.title = "My First FastAPI"
app.version = "0.0.1"

# register middleware para manejo de errores
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

# creamos el primer endpoint
@app.get("/", tags=["Home"])
def message():
    return HTMLResponse(content="<h1>Welcome to my API</h1>")

