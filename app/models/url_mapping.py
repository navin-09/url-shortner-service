import uuid
from sqlalchemy import Column, String, BigInteger, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base

class UrlMapping(Base):
    __tablename__ = "url_mapping"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_code = Column(String(10), nullable=False, unique=True, index=True)
    original_url = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    click_count = Column(BigInteger, nullable=False, default=0)
    last_accessed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
