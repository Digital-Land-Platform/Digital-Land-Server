from enum import Enum
import strawberry
from uuid import UUID
from typing import Optional, List
from sqlalchemy import DateTime, Text, Column, Integer, String, Float, ForeignKey
from src.graphql.property.types import PropertyStatusType

@strawberry.input
class PropertySearchInput:
    location: Optional[str] = None       
    min_price: Optional[float] = None    
    max_price: Optional[float] = None    
    min_size: Optional[float] = None     
    max_size: Optional[float] = None     
    status: Optional[PropertyStatusType] = None  
    page: int = 1                        
    limit: int = 10