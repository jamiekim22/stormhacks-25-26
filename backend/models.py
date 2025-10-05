from typing import Optional
from pydantic import BaseModel, Field, validator
import re

class Employee(BaseModel):
    """Employee data model matching the Snowflake table schema."""
    
    id: int = Field(..., description="Employee ID from database")
    name: str = Field(..., min_length=1, max_length=50, description="Employee full name")
    phone_number: Optional[str] = Field(None, max_length=15, description="Employee phone number")
    company: Optional[str] = Field(None, description="Company name (optional field)")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        """Validate phone number format if provided."""
        if v is None:
            return v
        
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', v)
        
        # Check if it's a valid length (10-15 digits)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be between 10 and 15 digits')
        
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name is not empty after stripping whitespace."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "phone_number": "1234567890",
                "company": "Acme Corp"
            }
        }

class CallSimulationRequest(BaseModel):
    """Request model for call simulation endpoint."""
    
    employee_id: int = Field(..., gt=0, description="ID of employee to call")
    scenario_type: str = Field(
        default="default", 
        description="Type of scam scenario to simulate",
        pattern="^(default|phishing|social_engineering|tech_support|financial)$"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "employee_id": 1,
                "scenario_type": "default"
            }
        }

class CallSimulationResponse(BaseModel):
    """Response model for call simulation endpoint."""
    
    call_id: str = Field(..., description="Unique identifier for the call session")
    status: str = Field(..., description="Status of the call initiation")
    message: str = Field(..., description="Human-readable message about the call status")
    employee_name: Optional[str] = Field(None, description="Name of employee being called")
    employee_phone: Optional[str] = Field(None, description="Phone number being called")
    
    class Config:
        schema_extra = {
            "example": {
                "call_id": "call_123456789",
                "status": "success",
                "message": "Call simulation initiated successfully",
                "employee_name": "John Doe",
                "employee_phone": "(123) 456-7890"
            }
        }

class CallStatusResponse(BaseModel):
    """Response model for call status endpoint."""
    
    call_id: str = Field(..., description="Call session identifier")
    status: str = Field(..., description="Current status of the call")
    details: Optional[dict] = Field(None, description="Additional call details")
    duration: Optional[int] = Field(None, description="Call duration in seconds")
    transcript: Optional[str] = Field(None, description="Call transcript if available")
    
    class Config:
        schema_extra = {
            "example": {
                "call_id": "call_123456789",
                "status": "completed",
                "details": {"confidence_score": 0.85},
                "duration": 120,
                "transcript": "Hello, this is a test call..."
            }
        }

class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "employee_not_found",
                "message": "Employee with ID 123 not found",
                "details": {"employee_id": 123}
            }
        }