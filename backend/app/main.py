from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.db import Base, engine
from .core.config import settings
from .api.routes.items import router as items_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.API_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,              # keep localhost entries
    allow_origin_regex=r"^https://.*\.streamlit\.app$",  # allow Streamlit Cloud
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)

@app.get("/")
def root():
    return {"status": "ok"}
