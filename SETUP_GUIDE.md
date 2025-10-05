# Development Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Node.js**: Version 18.0 or higher
- **Python**: Version 3.8 or higher
- **npm**: Comes with Node.js
- **pip**: Python package installer
- **Snowflake Account**: For database access

### Environment Setup

#### 1. Clone Repository
```bash
git clone https://github.com/jamiekim22/stormhacks-25-26.git
cd stormhacks-25-26
```

#### 2. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your Snowflake credentials
nano .env
```

**Required Environment Variables:**
```env
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=STORMHACKS25
SNOWFLAKE_SCHEMA=PUBLIC
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### 3. Frontend Setup
```bash
cd ../frontend

# Install Node.js dependencies
npm install

# Create environment file
cp .env.example .env.local

# Edit .env.local
nano .env.local
```

**Frontend Environment:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 4. Database Setup
```bash
# From project root, run database setup
cd backend
python -c "from database import db; print('Database connection:', db.test_connection())"

# Insert sample data (optional)
# Run the SQL files in your Snowflake console:
# - create_database.sql
# - create_security_tables.sql
# - fake_security_assessments.sql
```

### Running the Application

#### Start Backend Server
```bash
cd backend
python main.py

# Or with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### Start Frontend Development Server
```bash
cd frontend
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## 🛠️ Development Workflow

### Daily Development Routine

1. **Start Development Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend && python main.py
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

2. **Check API Health**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test Database Connection**
   ```bash
   curl http://localhost:8000/api/test-db
   ```

### Making Changes

#### Frontend Development
```bash
# Install new packages
npm install package-name

# Type checking
npm run type-check

# Build for production
npm run build

# Start production server
npm start
```

#### Backend Development
```bash
# Install new packages
pip install package-name
pip freeze > requirements.txt

# Run with debug mode
python main.py --debug

# Check API documentation
# Visit: http://localhost:8000/docs
```

### Code Quality

#### Frontend
```bash
# Type checking
npx tsc --noEmit

# Linting (if configured)
npm run lint

# Format code (if configured)
npm run format
```

#### Backend
```bash
# Code formatting with black
pip install black
black .

# Import sorting
pip install isort
isort .

# Type checking
pip install mypy
mypy .
```

---

## 🧪 Testing

### Frontend Testing
```bash
# Run tests (if configured)
npm test

# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage
```

### Backend Testing
```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_employees.py
```

### API Testing with curl

#### Employee Endpoints
```bash
# Get all employees
curl http://localhost:8000/api/employees

# Get specific employee
curl http://localhost:8000/api/employees/1

# Search employees
curl "http://localhost:8000/api/employees?search=john"
```

#### Security Assessment Endpoints
```bash
# Create assessment
curl -X POST http://localhost:8000/api/security-assessments \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "security_score": 75,
    "resistance_level": "Medium",
    "social_engineering_susceptibility": "Low",
    "feedback": "Test feedback",
    "scoring_explanation": "Test explanation"
  }'

# Get employee assessments
curl http://localhost:8000/api/employees/1/security-assessments
```

#### Call Simulation Endpoints
```bash
# Initiate call
curl -X POST http://localhost:8000/api/simulate-call \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "phone_number": "(555) 123-4567",
    "scenario_type": "default"
  }'

# Check call status
curl http://localhost:8000/api/call-status/call_abc123
```

---

## 🐛 Debugging

### Common Issues

#### Backend Issues

**Database Connection Error**
```bash
# Check environment variables
env | grep SNOWFLAKE

# Test connection manually
python -c "from database import db; db.test_connection()"
```

**CORS Error**
```bash
# Verify CORS origins in .env
echo $CORS_ORIGINS

# Check backend logs for CORS errors
tail -f backend.log
```

**Import Errors**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Frontend Issues

**API Connection Error**
```bash
# Check environment variable
echo $NEXT_PUBLIC_API_URL

# Verify backend is running
curl http://localhost:8000/health
```

**TypeScript Errors**
```bash
# Check types
npx tsc --noEmit

# Clear Next.js cache
rm -rf .next
npm run dev
```

**Module Not Found**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Debug Modes

#### Backend Debug Mode
```python
# In main.py, add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug
uvicorn main:app --reload --log-level debug
```

#### Frontend Debug Mode
```bash
# Enable debug mode
DEBUG=1 npm run dev

# Check browser console for errors
# Open Developer Tools > Console
```

---

## 📦 Deployment

### Production Build

#### Frontend
```bash
cd frontend
npm run build
npm start
```

#### Backend
```bash
cd backend

# Install production dependencies
pip install -r requirements.txt

# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Variables for Production

Update `.env` files with production values:
- Change database credentials
- Update CORS origins to production domains
- Set proper API URLs
- Configure logging levels

### Docker Deployment (Optional)

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 🔧 IDE Configuration

### VS Code Settings
```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "typescript.preferences.quoteStyle": "single",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

### Recommended Extensions
- **Frontend**: ES7+ React/Redux/React-Native snippets, Tailwind CSS IntelliSense
- **Backend**: Python, Pylance, autoDocstring
- **General**: GitLens, Prettier, ESLint

---

## 📚 Additional Resources

### Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Snowflake Python Connector](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Community
- [StormHacks Discord](#)
- [Project GitHub Issues](https://github.com/jamiekim22/stormhacks-25-26/issues)

### Support
If you encounter issues:
1. Check this documentation
2. Search existing GitHub issues
3. Create a new issue with detailed error information
4. Contact the development team