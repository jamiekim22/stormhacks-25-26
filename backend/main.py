from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
import uuid
from datetime import datetime

from models import (
    Employee, 
    CallSimulationRequest, 
    CallSimulationResponse, 
    CallStatusResponse,
)
from repository import employee_repo
from snowflake.connector.errors import DatabaseError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Employee Voice Simulation API",
    description="API for managing employees and simulating scam calls",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(DatabaseError)
async def database_exception_handler(request, exc):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "database_error",
            "message": "Database operation failed",
            "details": {"error": str(exc)}
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "message": str(exc)
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Employee endpoints
@app.get("/api/employees", response_model=List[Employee])
async def get_all_employees(search: Optional[str] = None):
    """
    Get all employees or search employees by name/phone.
    
    Args:
        search: Optional search term to filter employees
        
    Returns:
        List of Employee objects
    """
    try:
        logger.info(f"Fetching employees with search term: {search}")
        
        if search:
            employees = employee_repo.search_employees(search.strip())
        else:
            employees = employee_repo.get_all_employees()
        
        logger.info(f"Returning {len(employees)} employees")
        return employees
        
    except DatabaseError as e:
        logger.error(f"Database error in get_all_employees: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "database_error",
                "message": "Failed to fetch employees from database"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_all_employees: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred"
            }
        )

@app.get("/api/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int):
    """
    Get a specific employee by ID.
    
    Args:
        employee_id: The employee's ID
        
    Returns:
        Employee object
        
    Raises:
        HTTPException: If employee not found
    """
    try:
        logger.info(f"Fetching employee {employee_id}")
        
        employee = employee_repo.get_employee_by_id(employee_id)
        
        if not employee:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "employee_not_found",
                    "message": f"Employee with ID {employee_id} not found",
                    "details": {"employee_id": employee_id}
                }
            )
        
        logger.info(f"Returning employee: {employee.name}")
        return employee
        
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(f"Database error in get_employee: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "database_error",
                "message": "Failed to fetch employee from database"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_employee: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred"
            }
        )

@app.post("/api/simulate-call", response_model=CallSimulationResponse)
async def simulate_call(
    request: CallSimulationRequest,
    background_tasks: BackgroundTasks
):
    """
    Initiate a scam call simulation to an employee.
    
    Args:
        request: Call simulation request containing employee_id and scenario_type
        background_tasks: FastAPI background tasks for async call execution
        
    Returns:
        CallSimulationResponse with call details
        
    Raises:
        HTTPException: If employee not found or call initiation fails
    """
    try:
        logger.info(f"Initiating call simulation for employee {request.employee_id}")
        
        # Validate employee exists
        employee = employee_repo.get_employee_by_id(request.employee_id)
        if not employee:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "employee_not_found",
                    "message": f"Employee with ID {request.employee_id} not found",
                    "details": {"employee_id": request.employee_id}
                }
            )
        
        # Validate employee has phone number
        if not employee.phone_number:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "no_phone_number",
                    "message": f"Employee {employee.name} does not have a phone number",
                    "details": {"employee_id": request.employee_id}
                }
            )
        
        # Generate unique call ID
        call_id = f"call_{uuid.uuid4().hex[:12]}"
        
        # Start call simulation in background
        background_tasks.add_task(
            call_service.start_call_simulation,
            call_id,
            employee,
            request.scenario_type
        )
        
        response = CallSimulationResponse(
            call_id=call_id,
            status="initiated",
            message=f"Call simulation initiated for {employee.name}",
            employee_name=employee.name,
            employee_phone=employee.phone_number
        )
        
        logger.info(f"Call simulation {call_id} initiated for {employee.name}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in simulate_call: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "call_initiation_failed",
                "message": "Failed to initiate call simulation",
                "details": {"error": str(e)}
            }
        )

@app.get("/api/call-status/{call_id}", response_model=CallStatusResponse)
async def get_call_status(call_id: str):
    """
    Get the status of a call simulation.
    
    Args:
        call_id: The unique call identifier
        
    Returns:
        CallStatusResponse with current call status
        
    Raises:
        HTTPException: If call not found
    """
    try:
        logger.info(f"Fetching status for call {call_id}")
        
        call_status = call_service.get_call_status(call_id)
        
        if not call_status:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "call_not_found",
                    "message": f"Call with ID {call_id} not found",
                    "details": {"call_id": call_id}
                }
            )
        
        return call_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_call_status: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "status_fetch_failed",
                "message": "Failed to fetch call status",
                "details": {"error": str(e)}
            }
        )

# Additional utility endpoints
@app.get("/api/employees/count")
async def get_employee_count():
    """Get the total count of employees in the database."""
    try:
        employees = employee_repo.get_all_employees()
        return {"count": len(employees)}
    except Exception as e:
        logger.error(f"Error getting employee count: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "count_failed",
                "message": "Failed to get employee count"
            }
        )

# Development endpoints (can be removed in production)
@app.get("/api/test-db")
async def test_database_connection():
    """Test database connectivity (development endpoint)."""
    try:
        from database import db
        is_connected = db.test_connection()
        return {
            "database_connected": is_connected,
            "message": "Database connection successful" if is_connected else "Database connection failed"
        }
    except Exception as e:
        logger.error(f"Database test error: {e}")
        return {
            "database_connected": False,
            "message": f"Database test failed: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)