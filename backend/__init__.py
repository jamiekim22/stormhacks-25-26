"""
Backend package initialization.
"""

from database import db
from models import Employee, CallSimulationRequest, CallSimulationResponse
from repository import employee_repo
from call_service import call_service

__version__ = "1.0.0"
__all__ = ["db", "Employee", "CallSimulationRequest", "CallSimulationResponse", "employee_repo", "call_service"]