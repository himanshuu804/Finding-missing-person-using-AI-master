from typing import Optional
from sqlmodel import SQLModel, Field


class MissingPerson(SQLModel, table=True):
    __tablename__ = "missing_persons"
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    location_last_seen: Optional[str] = None
    birth_marks: Optional[str] = None
    face_mesh: Optional[str] = None
    registered_by: Optional[str] = None
    status: str = "NF"  # NF = Not Found, F = Found
    image_path: Optional[str] = None
    contact_number: Optional[str] = None
    description: Optional[str] = None


class PublicSubmissions(SQLModel, table=True):
    __tablename__ = "public_submissions"
    id: Optional[str] = Field(default=None, primary_key=True)
    submitted_by: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    face_mesh: Optional[str] = None
    birth_marks: Optional[str] = None
    status: str = "NF"
    image_path: Optional[str] = None
