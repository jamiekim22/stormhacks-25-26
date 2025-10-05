# Project Structure Documentation

## 📁 Directory Overview

```
stormhacks-25-26/
├── frontend/                 # Next.js React application
├── backend/                  # FastAPI Python server
├── Speech to Speech/         # Voice processing pipeline
├── twilio_openai_tutorial/   # Twilio integration examples
├── twilio_poc/              # Twilio proof of concept
├── urlDynamicCalls/         # Dynamic call URL handling
├── *.sql                    # Database schema and test data
├── *.py                     # Root level Python utilities
└── documentation files
```

## 🎨 Frontend Structure (`frontend/`)

```
frontend/
├── src/
│   ├── app/                 # Next.js 13+ App Router
│   │   ├── employees/       # Employee management page
│   │   ├── voice-simulations/ # Call simulation interface
│   │   ├── analytics/       # Analytics dashboard
│   │   ├── campaigns/       # Campaign management
│   │   ├── training-modules/ # Training content
│   │   ├── settings/        # Application settings
│   │   ├── help/           # Help and documentation
│   │   ├── globals.css     # Global styles and CSS variables
│   │   ├── layout.tsx      # Root layout component
│   │   └── page.tsx        # Home page
│   ├── components/          # Reusable React components
│   │   └── PageTemplate.tsx # Consistent page layout
│   ├── api/                # API service functions
│   │   └── employeeService.ts # Employee-related API calls
│   └── types/              # TypeScript type definitions
│       ├── Employee.ts     # Employee interface
│       └── SecurityAssessment.ts # Assessment interface
├── public/                 # Static assets (SVGs, images)
├── package.json           # Dependencies and scripts
├── next.config.ts         # Next.js configuration
├── tsconfig.json         # TypeScript configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── postcss.config.mjs    # PostCSS configuration
```

### Key Frontend Components

#### `PageTemplate.tsx`
Provides consistent layout across all pages with:
- Header with title and description
- Dark theme styling
- Responsive design
- Consistent spacing and typography

#### `employees/page.tsx`
Employee management interface featuring:
- Employee dropdown selector
- Security assessment history table
- Color-coded performance metrics
- Real-time data fetching

#### `voice-simulations/page.tsx`
Call simulation interface with:
- Employee directory table
- Click-to-call functionality
- Phone icon buttons
- Real-time call initiation

### Styling System

#### CSS Custom Properties
Defined in `globals.css`:
```css
--color-background: #050b16
--color-surface: #111a24
--color-accent: #3b82f6
--color-text-muted: #94a3b8
```

#### Tailwind Integration
- Utility-first CSS framework
- Custom color scheme integration
- Responsive design patterns
- Component-specific styling

## 🔧 Backend Structure (`backend/`)

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic data models
├── repository.py        # Database access layer
├── database.py          # Snowflake connection management
├── config.py           # Application configuration
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── .env.example       # Environment template
└── __pycache__/       # Python bytecode cache
```

### Backend Architecture

#### `main.py` - API Server
- FastAPI application setup
- CORS middleware configuration
- Route definitions and handlers
- Error handling and logging
- Background task management

#### `models.py` - Data Models
```python
# Core models defined:
- Employee              # Employee data structure
- SecurityAssessment    # Assessment input model
- SecurityAssessmentResponse # Assessment output model
- CallSimulationRequest # Call initiation request
- CallSimulationResponse # Call response data
- ErrorResponse         # Standardized error format
```

#### `repository.py` - Data Access
```python
# Repository classes:
- EmployeeRepository           # Employee CRUD operations
- SecurityAssessmentRepository # Assessment data management
```

#### `database.py` - Connection Layer
- Snowflake connector management
- Connection pooling
- Query execution utilities
- Error handling and logging

### API Route Structure

```
Health & Utility:
├── GET  /health                    # Health check
└── GET  /api/test-db              # Database connectivity test

Employee Management:
├── GET  /api/employees            # List all employees
├── GET  /api/employees/{id}       # Get specific employee
└── GET  /api/employees/count      # Employee count

Security Assessments:
├── POST /api/security-assessments # Create assessment
└── GET  /api/employees/{id}/security-assessments # Get employee assessments

Voice Simulation:
├── POST /api/simulate-call        # Initiate call
└── GET  /api/call-status/{id}     # Call status
```

## 🗃️ Database Structure

### Snowflake Schema
```sql
Database: STORMHACKS25
Schema: PUBLIC

Tables:
├── Employees                    # Employee directory
├── SecurityAssessments         # Assessment results
├── DataCollected              # Compromised data tracking
├── OtherInfoCollected         # Additional breach data
├── KeyMistakes               # Common security mistakes
└── SuccessfulDefenses        # Positive security behaviors
```

### Table Relationships
```
Employees (1) ──── (Many) SecurityAssessments
     │
     └── Assessment Data:
         ├── DataCollected
         ├── KeyMistakes
         └── SuccessfulDefenses
```

## 🎤 Speech Pipeline (`Speech to Speech/`)

```
Speech to Speech/
├── s2s_pipeline.py           # Main speech processing pipeline
├── s2s_pipeline_simplified.py # Simplified version
├── listen_and_play.py        # Audio I/O handling
├── baseHandler.py           # Base processing class
├── startup.py              # Pipeline initialization
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Container orchestration
├── Dockerfile             # Container configuration
├── arguments_classes/      # Configuration classes
├── connections/           # Audio connection handlers
├── LLM/                  # Language model integration
├── STT/                  # Speech-to-text modules
├── TTS/                  # Text-to-speech modules
├── VAD/                  # Voice activity detection
├── utils/                # Utility functions
└── cache/                # Temporary file storage
```

### Speech Processing Flow
```
Audio Input → STT → LLM Processing → TTS → Audio Output
     ↓           ↓           ↓           ↓
   Voice      Text       Response    Voice
Activity   Recognition  Generation  Synthesis
Detection
```

## 🔌 Integration Points

### Frontend ↔ Backend
- REST API communication
- JSON data exchange
- Error handling and user feedback
- Real-time status updates

### Backend ↔ Database
- Snowflake connector
- Parameterized queries
- Connection pooling
- Transaction management

### Backend ↔ Speech Pipeline
- Process spawning for call simulation
- Inter-process communication
- Status tracking and monitoring
- Resource management

## 📦 Configuration Management

### Environment Variables
```
Backend (.env):
├── SNOWFLAKE_*          # Database credentials
├── CORS_ORIGINS         # Frontend URL whitelist
├── API_*               # Server configuration
├── SPEECH_PIPELINE_*   # Voice processing settings
└── LOG_*               # Logging configuration

Frontend (.env.local):
└── NEXT_PUBLIC_API_URL # Backend API endpoint
```

### Configuration Files
```
Frontend:
├── next.config.ts      # Next.js settings
├── tailwind.config.js  # Styling framework
├── tsconfig.json      # TypeScript compiler
└── package.json       # Dependencies and scripts

Backend:
├── requirements.txt   # Python packages
└── config.py         # Application settings

Speech Pipeline:
├── config_*.json     # Pipeline configurations
├── docker-compose.yml # Container settings
└── requirements*.txt  # Environment-specific packages
```

## 🔄 Data Flow

### Call Simulation Flow
```
1. Frontend: User clicks call button
2. Frontend: POST /api/simulate-call
3. Backend: Validates employee and phone number
4. Backend: Spawns speech pipeline process
5. Speech Pipeline: Initiates voice call
6. Backend: Returns call ID and status
7. Frontend: Displays success/error message
8. Background: Call processing continues
```

### Assessment Creation Flow
```
1. External System: Generates assessment data
2. External System: POST /api/security-assessments
3. Backend: Validates employee exists
4. Backend: Validates assessment data
5. Database: Inserts new assessment record
6. Backend: Returns created assessment
7. Frontend: Can retrieve via employee assessments endpoint
```

### Employee Data Access Flow
```
1. Frontend: Loads employee page
2. Frontend: GET /api/employees
3. Backend: Queries Snowflake database
4. Database: Returns employee records
5. Backend: Formats as JSON response
6. Frontend: Renders employee table
7. User: Selects employee from dropdown
8. Frontend: GET /api/employees/{id}/security-assessments
9. Backend: Retrieves assessment history
10. Frontend: Displays assessment table
```

## 🧪 Testing Structure

### Test Data Files
```
├── fake_security_assessments.sql  # Sample assessment data
├── create_database.sql           # Database schema
└── create_security_tables.sql    # Security-specific tables
```

### Testing Scenarios
- Employee CRUD operations
- Assessment creation and retrieval
- Call simulation initiation
- Error handling and validation
- Cross-origin request handling

## 🚀 Deployment Structure

### Development
```
Frontend: localhost:3000
Backend:  localhost:8000
Database: Snowflake cloud instance
```

### Production Considerations
- Environment variable management
- CORS origin updates
- Database connection scaling
- Container orchestration
- Load balancing configuration
- SSL/TLS certificate setup
- Monitoring and logging integration