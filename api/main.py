import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import lifespan

from api.dependencies.database import SessionLocal
from api.seed import seed_data
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf

app = FastAPI()


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    seed_data(db)
    db.close()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)