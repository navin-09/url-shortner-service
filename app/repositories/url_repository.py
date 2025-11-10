from sqlalchemy import insert, select, update, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.url_mapping import UrlMapping

class UrlRepository:
    """Interface-like base to clarify contract."""
    def create_if_not_exists(self, db: Session, short_code: str, original_url: str) -> UrlMapping: ...
    def get_by_code(self, db: Session, code: str) -> UrlMapping | None: ...
    def get_by_original(self, db: Session, url: str) -> UrlMapping | None: ...
    def increment_click(self, db: Session, code: str) -> None: ...

class PostgresUrlRepository(UrlRepository):
    """Concrete implementation with ACID-safe insert logic."""

    def create_if_not_exists(self, db: Session, short_code: str, original_url: str) -> UrlMapping:
        # Check if original already exists (idempotency)
        existing = db.execute(select(UrlMapping).where(UrlMapping.original_url == original_url)).scalar_one_or_none()
        if existing:
            return existing

        stmt = insert(UrlMapping).values(short_code=short_code, original_url=original_url)
        try:
            db.execute(stmt)
            db.commit()
        except IntegrityError:
            db.rollback()
            # possible collision or race
            existing = db.execute(select(UrlMapping).where(UrlMapping.original_url == original_url)).scalar_one_or_none()
            if existing:
                return existing
            raise
        return db.execute(select(UrlMapping).where(UrlMapping.short_code == short_code)).scalar_one()

    def get_by_code(self, db: Session, code: str) -> UrlMapping | None:
        return db.execute(select(UrlMapping).where(UrlMapping.short_code == code)).scalar_one_or_none()

    def get_by_original(self, db: Session, url: str) -> UrlMapping | None:
        return db.execute(select(UrlMapping).where(UrlMapping.original_url == url)).scalar_one_or_none()

    def increment_click(self, db: Session, code: str) -> None:
        db.execute(
            update(UrlMapping)
            .where(UrlMapping.short_code == code)
            .values(click_count=UrlMapping.click_count + 1, last_accessed_at=func.now())
        )
        db.commit()
