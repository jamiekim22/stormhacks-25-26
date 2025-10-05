#!/usr/bin/env python3
"""
Production server startup script for the Employee Voice Simulation API.
"""

import sys
import os
import logging
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from config import settings
from main import app

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT
    )

def validate_environment():
    """Validate required environment variables."""
    missing = settings.validate()
    if missing:
        logging.error(f"Missing required environment variables: {', '.join(missing)}")
        logging.error("Please check your .env file or environment configuration")
        sys.exit(1)

def main():
    """Main server startup function."""
    print("🚀 Starting Employee Voice Simulation API...")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Validate environment
        validate_environment()
        logger.info("Environment validation passed")
        
        # Test database connection
        from database import db
        if db.test_connection():
            logger.info("✅ Database connection successful")
        else:
            logger.error("❌ Database connection failed")
            sys.exit(1)
        
        # Start the server
        import uvicorn
        
        logger.info(f"Starting server on {settings.API_HOST}:{settings.API_PORT}")
        logger.info(f"Debug mode: {settings.DEBUG}")
        logger.info(f"Docs enabled: {settings.ENABLE_DOCS}")
        
        uvicorn.run(
            "main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=settings.API_RELOAD and settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()