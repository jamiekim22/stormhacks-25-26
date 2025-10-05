# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required for API endpoints. In production, implement proper authentication and authorization.

## Error Responses
All endpoints return standardized error responses:

```json
{
  "error": "error_type",
  "message": "Human-readable error message",
  "details": {
    "additional": "context"
  }
}
```

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-05T14:30:00.000Z"
}
```

---

### Employee Management

#### GET /api/employees
Retrieve all employees or search by name/phone.

**Query Parameters:**
- `search` (optional): Search term to filter employees

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone_number": "(555) 123-4567"
  }
]
```

**Error Codes:**
- `500`: Database error

---

#### GET /api/employees/{employee_id}
Retrieve a specific employee by ID.

**Path Parameters:**
- `employee_id`: Integer - Employee's unique identifier

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone_number": "(555) 123-4567"
}
```

**Error Codes:**
- `404`: Employee not found
- `500`: Database error

---

#### GET /api/employees/count
Get total count of employees.

**Response:**
```json
{
  "count": 150
}
```

---

### Security Assessments

#### POST /api/security-assessments
Create a new security assessment for an employee.

**Request Body:**
```json
{
  "employee_id": 1,
  "security_score": 75,
  "resistance_level": "Medium",
  "social_engineering_susceptibility": "Low",
  "feedback": "Employee showed good awareness but fell for phishing attempt",
  "scoring_explanation": "Score based on response time and verification attempts"
}
```

**Field Validations:**
- `employee_id`: Must exist in database
- `security_score`: Integer 0-100
- `resistance_level`: Must be "Low", "Medium", or "High"
- `social_engineering_susceptibility`: Must be "Low", "Medium", or "High"
- `feedback`: Optional text
- `scoring_explanation`: Optional text

**Response:**
```json
{
  "id": 123,
  "employee_id": 1,
  "assessment_date": "2025-10-05 14:30:00",
  "security_score": 75,
  "resistance_level": "Medium",
  "social_engineering_susceptibility": "Low",
  "feedback": "Employee showed good awareness but fell for phishing attempt",
  "scoring_explanation": "Score based on response time and verification attempts"
}
```

**Error Codes:**
- `400`: Employee doesn't exist or validation error
- `500`: Database error

---

#### GET /api/employees/{employee_id}/security-assessments
Get all security assessments for a specific employee.

**Path Parameters:**
- `employee_id`: Integer - Employee's unique identifier

**Response:**
```json
[
  {
    "id": 123,
    "employee_id": 1,
    "assessment_date": "2025-10-05 14:30:00",
    "security_score": 75,
    "resistance_level": "Medium",
    "social_engineering_susceptibility": "Low",
    "feedback": "Employee showed good awareness but fell for phishing attempt",
    "scoring_explanation": "Score based on response time and verification attempts"
  }
]
```

**Error Codes:**
- `404`: Employee not found
- `500`: Database error

---

### Voice Simulation

#### POST /api/simulate-call
Initiate a scam call simulation to an employee.

**Request Body:**
```json
{
  "employee_id": 1,
  "phone_number": "(555) 123-4567",
  "scenario_type": "default"
}
```

**Field Validations:**
- `employee_id`: Must exist in database
- `phone_number`: Required, must be valid phone number
- `scenario_type`: Must be one of: "default", "phishing", "social_engineering", "tech_support", "financial"

**Response:**
```json
{
  "call_id": "call_abc123def456",
  "status": "initiated",
  "message": "Call simulation initiated for John Doe",
  "employee_name": "John Doe",
  "employee_phone": "(555) 123-4567"
}
```

**Error Codes:**
- `404`: Employee not found
- `400`: Missing phone number or validation error
- `500`: Call initiation failed

---

#### GET /api/call-status/{call_id}
Get the current status of a call simulation.

**Path Parameters:**
- `call_id`: String - Unique call identifier

**Response:**
```json
{
  "call_id": "call_abc123def456",
  "status": "completed",
  "details": {
    "confidence_score": 0.85
  },
  "duration": 120,
  "transcript": "Hello, this is a test call..."
}
```

**Possible Status Values:**
- `initiated`: Call has been started
- `ringing`: Phone is ringing
- `connected`: Call is active
- `completed`: Call finished successfully
- `failed`: Call failed
- `cancelled`: Call was cancelled

**Error Codes:**
- `404`: Call not found
- `500`: Status fetch failed

---

### Development Endpoints

#### GET /api/test-db
Test database connectivity (development only).

**Response:**
```json
{
  "database_connected": true,
  "message": "Database connection successful"
}
```

---

## Rate Limiting
Currently no rate limiting is implemented. Consider adding rate limiting for production use:
- Employee endpoints: 100 requests/minute
- Call simulation: 10 requests/minute per IP
- Assessment creation: 50 requests/minute

## CORS Configuration
API accepts requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Update CORS origins in production to match your domain.

## Database Connection
The API uses Snowflake as the primary database. Ensure proper connection parameters are set in the environment variables.

## Logging
All API requests and errors are logged. Check the application logs for debugging information.

## Performance Considerations
- Employee list endpoint may be slow with large datasets
- Consider implementing pagination for large result sets
- Database connection pooling is implemented for better performance
- Background tasks are used for call simulations to avoid blocking

## Security Notes
- Implement authentication before production deployment
- Add input sanitization for all user inputs
- Use HTTPS in production
- Implement proper error handling that doesn't leak sensitive information
- Add request validation middleware
- Consider implementing API key authentication for call simulation endpoints