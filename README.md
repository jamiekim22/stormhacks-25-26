# StormHacks 2025 - Employee Security Assessment Platform

## 🎯 Project Overview

A comprehensive cybersecurity training platform that simulates social engineering attacks through voice calls and tracks employee security awareness through detailed assessments. Built for organizations to test and improve their employees' resistance to scam calls and social engineering tactics.

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 15.5.4 with TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python
- **Database**: Snowflake Data Warehouse
- **Voice Processing**: Custom Speech-to-Speech pipeline
- **Icons**: Lucide React
- **Styling**: CSS Custom Properties (Dark Theme)

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Snowflake DB  │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Data Store)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Speech Pipeline │
                       │ (Voice Calls)   │
                       └─────────────────┘
```

## 🚀 Features

### 📊 Employee Management
- **Employee Directory**: View all employees with contact information
- **Search & Filter**: Find employees by name or phone number
- **Database Integration**: Real-time sync with Snowflake database

### 📞 Voice Simulation System
- **Scam Call Simulation**: Automated voice calls simulating various attack scenarios
- **Real-time Call Initiation**: Click-to-call functionality from employee table
- **Call Status Tracking**: Monitor ongoing and completed call simulations
- **Multiple Scenarios**: Support for phishing, social engineering, tech support, and financial scams

### 🛡️ Security Assessment Tracking
- **Assessment Creation**: Record detailed security assessment results
- **Performance Metrics**: Track security scores, resistance levels, and susceptibility
- **Historical Data**: View assessment history for each employee
- **Detailed Feedback**: Store comprehensive feedback and scoring explanations

### 📈 Analytics Dashboard
- **Employee Performance**: Individual employee security assessment history
- **Color-coded Scoring**: Visual indicators for performance levels
  - 🟢 Green (80-100): Excellent security awareness
  - 🟡 Yellow (60-79): Moderate security awareness
  - 🔴 Red (0-59): Needs improvement
- **Trend Analysis**: Track improvement over time

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Snowflake Account
- Environment variables configured

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Environment Configuration
Create `.env` files in both frontend and backend directories:

**Backend `.env`:**
```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=STORMHACKS25
SNOWFLAKE_SCHEMA=PUBLIC
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Frontend `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📋 API Documentation

### Employee Endpoints

#### Get All Employees
```http
GET /api/employees
```
Returns list of all employees with ID, name, and phone number.

#### Get Employee by ID
```http
GET /api/employees/{employee_id}
```
Returns specific employee details.

### Security Assessment Endpoints

#### Create Security Assessment
```http
POST /api/security-assessments
```
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

#### Get Employee Assessments
```http
GET /api/employees/{employee_id}/security-assessments
```
Returns all security assessments for a specific employee.

### Voice Simulation Endpoints

#### Initiate Call Simulation
```http
POST /api/simulate-call
```
**Request Body:**
```json
{
  "employee_id": 1,
  "phone_number": "(555) 123-4567",
  "scenario_type": "default"
}
```

#### Get Call Status
```http
GET /api/call-status/{call_id}
```
Returns current status of a call simulation.

## 🗃️ Database Schema

### Employees Table
```sql
CREATE TABLE Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15)
);
```

### SecurityAssessments Table
```sql
CREATE TABLE SecurityAssessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    security_score INT NOT NULL,
    resistance_level ENUM('Low', 'Medium', 'High') NOT NULL,
    social_engineering_susceptibility ENUM('Low', 'Medium', 'High') NOT NULL,
    feedback TEXT,
    scoring_explanation TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employees(id) ON DELETE CASCADE
);
```

## 🎨 UI Components

### Design System
- **Dark Theme**: Custom CSS properties for consistent styling
- **Color Palette**:
  - Background: `#050b16`
  - Surface: `#111a24`
  - Accent: `#3b82f6`
  - Text: `#f8fafc`
  - Muted: `#94a3b8`

### Key Components
- **PageTemplate**: Consistent layout wrapper
- **Employee Table**: Sortable, filterable employee directory
- **Dropdown Selector**: Employee selection interface
- **Assessment Display**: Color-coded performance metrics
- **Call Button**: One-click call initiation

## 🔧 Development Workflow

### Frontend Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run type checking
npm run type-check
```

### Backend Development
```bash
# Start FastAPI development server
python main.py

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Operations
```bash
# Run database migrations
python -c "from database import db; db.test_connection()"

# Insert test data
# Use the provided fake_security_assessments.sql file
```

## 🧪 Testing

### Sample Data
Use the provided `fake_security_assessments.sql` to populate test data:
- Employee 1: Shows improvement over time (35 → 58 → 82)
- Employee 2: Mixed performance with recovery (67 → 52 → 74)

### Testing Scenarios
1. **Employee Management**: Add, view, search employees
2. **Call Simulation**: Initiate calls for different employees
3. **Assessment Tracking**: Create and view security assessments
4. **Error Handling**: Test with invalid data and network issues

## 🚨 Security Features

### Data Protection
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: Parameterized queries
- **CORS Configuration**: Restricted origins for API access
- **Error Handling**: Secure error messages without data leakage

### Assessment Criteria
- **Security Score**: 0-100 scale based on employee response
- **Resistance Level**: Low/Medium/High classification
- **Susceptibility Rating**: Likelihood to fall for social engineering
- **Detailed Feedback**: Specific improvement recommendations

## 🎯 Use Cases

### For Security Teams
- **Phishing Simulation**: Test employee email security awareness
- **Vishing Attacks**: Voice-based social engineering tests
- **Performance Tracking**: Monitor team security improvements
- **Training Identification**: Identify employees needing additional training

### For HR Departments
- **Onboarding Assessment**: Test new employee security awareness
- **Compliance Reporting**: Generate security training reports
- **Risk Assessment**: Identify high-risk employees or departments
- **Progress Monitoring**: Track improvement after training sessions

## 🔮 Future Enhancements

### Planned Features
- **Real-time Call Analytics**: Live call monitoring and analysis
- **Advanced Scenarios**: Industry-specific attack simulations
- **Reporting Dashboard**: Comprehensive analytics and insights
- **Integration APIs**: Connect with existing HR and security systems
- **Mobile App**: Native mobile application for on-the-go management

### Technical Improvements
- **WebSocket Integration**: Real-time call status updates
- **Caching Layer**: Redis for improved performance
- **Containerization**: Docker deployment configuration
- **CI/CD Pipeline**: Automated testing and deployment
- **Load Balancing**: Support for high-traffic scenarios

## 👥 Team

Built for StormHacks 2025 by Team [Your Team Name]

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation for common solutions

---

**Built with ❤️ for StormHacks 2025**