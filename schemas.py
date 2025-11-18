"""
Database Schemas for All Male Area (AMA)

Each Pydantic model corresponds to a MongoDB collection. The collection name is the
lowercased class name (e.g., Program -> "program").
"""

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class Program(BaseModel):
    title: str = Field(..., description="Program title")
    slug: str = Field(..., description="URL-friendly identifier")
    essence: str = Field(..., description="One sentence essence of the program")
    who: Optional[str] = Field(None, description="Who this is for")
    expect: Optional[List[str]] = Field(default_factory=list, description="What to expect bullets")
    duration: Optional[str] = Field(None, description="Duration e.g., '1 evening', '2 days'")
    order: int = Field(0, description="Sort order")


class Event(BaseModel):
    program_slug: str = Field(..., description="Link to Program via slug")
    title: str = Field(..., description="Event title shown to users")
    city: Optional[str] = Field(None, description="City/Location")
    starts_at: datetime = Field(..., description="Start date and time (UTC)")
    ends_at: Optional[datetime] = Field(None, description="End date and time (UTC)")
    capacity: Optional[int] = Field(None, description="Capacity limit")
    price_huf: Optional[int] = Field(None, description="Price in HUF")


class Leader(BaseModel):
    name: str = Field(..., description="Leader name")
    stance: Optional[str] = Field(None, description="One-line stance")
    bio: Optional[str] = Field(None, description="Short, grounded bio")
    photo_url: Optional[str] = Field(None, description="Portrait URL")


class Testimonial(BaseModel):
    text: str = Field(..., description="Short, raw quote")
    author: Optional[str] = Field(None, description="Name or initials")
    age: Optional[int] = Field(None, description="Age")
    city: Optional[str] = Field(None, description="City")


class FAQ(BaseModel):
    q: str
    a: str


class Registration(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    program_slug: Optional[str] = None
    intention: Optional[str] = None

