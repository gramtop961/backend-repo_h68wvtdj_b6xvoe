"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Limited Edition Tees app schemas

class Tee(BaseModel):
    """
    Limited edition t-shirt drops
    Collection name: "tee"
    """
    name: str = Field(..., description="Tee name")
    slug: str = Field(..., description="URL-friendly identifier")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in USD")
    image: HttpUrl = Field(..., description="Primary image URL")
    gallery: Optional[List[HttpUrl]] = Field(default=None, description="Optional gallery images")
    colorway: Optional[str] = Field(default=None, description="Colorway or theme")
    release_month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="Release month in YYYY-MM")
    status: str = Field("current", description="current or archived")
    tags: Optional[List[str]] = Field(default=None, description="Style tags")

class Subscriber(BaseModel):
    """
    Newsletter / drop notifications subscribers
    Collection name: "subscriber"
    """
    email: EmailStr = Field(..., description="Subscriber email")
    name: Optional[str] = Field(default=None, description="Optional name")
    source: Optional[str] = Field(default="website", description="Signup source")
