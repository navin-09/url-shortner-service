from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.url_schema import UrlCreateRequest, UrlCreateResponse
from app.repositories.url_repository import PostgresUrlRepository
from app.services.shortener_service import UrlService
from app.core.db import get_db
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["URLs"])

repo = PostgresUrlRepository()
service = UrlService(repo, base_url=settings.BASE_URL)

@router.post("/urls", response_model=UrlCreateResponse)
def create_short_url(request_data: UrlCreateRequest, db: Session = Depends(get_db)):
    try:
        short_url, short_code = service.create_short_url(db, request_data.original_url)
        return UrlCreateResponse(short_code=short_code, short_url=short_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{short_code}")
def redirect_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    target = service.resolve_short_code(db, short_code)
    if not target:
        raise HTTPException(status_code=404, detail="Short code not found")
    return {"redirect_to": target}  # Replace with actual RedirectResponse later
