from fastapi import FastAPI
from app.api.routes_urls import router as urls_router

from app.core.db import Base, engine
from app.models import url_mapping  # ensure import
Base.metadata.create_all(bind=engine)


app = FastAPI(title="URL Shortener Service", version="1.0.0")
app.include_router(urls_router)

@app.get("/health")
def health():
    return {"status": "ok"}
