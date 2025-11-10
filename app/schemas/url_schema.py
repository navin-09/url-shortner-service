from pydantic import BaseModel, HttpUrl

class UrlCreateRequest(BaseModel):
    original_url: HttpUrl

class UrlCreateResponse(BaseModel):
    short_code: str
    short_url: str

class UrlInfoResponse(BaseModel):
    original_url: str
    click_count: int
    created_at: str
