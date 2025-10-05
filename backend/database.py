import os
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import snowflake.connector
from snowflake.connector import DictCursor
from snowflake.connector.errors import DatabaseError, ProgrammingError

logger = logging.getLogger(__name__)

class SnowflakeConnection:
    """
    Snowflake database connection manager with connection pooling and error handling.
    """
    
    def __init__(self):
        self.connection_params = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
        }
        
        # Validate required environment variables
        self._validate_connection_params()
    
    def _validate_connection_params(self) -> None:
        """Validate that all required connection parameters are present."""
        required_params = ['account', 'user', 'password', 'database']
        missing_params = [param for param in required_params if not self.connection_params.get(param)]
        
        if missing_params:
            raise ValueError(f"Missing required Snowflake connection parameters: {', '.join(missing_params)}")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for getting a database connection.
        Automatically handles connection cleanup.
        """
        connection = None
        try:
            connection = snowflake.connector.connect(**self.connection_params)
            logger.info("Successfully connected to Snowflake")
            yield connection
        except DatabaseError as e:
            logger.error(f"Database connection error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to Snowflake: {e}")
            raise
        finally:
            if connection:
                connection.close()
                logger.info("Snowflake connection closed")
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as a list of dictionaries.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            List of dictionaries representing query results
            
        Raises:
            DatabaseError: If there's an error executing the query
        """
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor(DictCursor)
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                results = cursor.fetchall()
                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results
                
            except ProgrammingError as e:
                logger.error(f"SQL programming error: {e}")
                raise DatabaseError(f"Query execution failed: {e}")
            except Exception as e:
                logger.error(f"Unexpected error executing query: {e}")
                raise
            finally:
                cursor.close()
    
    def execute_single_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a query that should return a single row.
        
        Args:
            query: SQL query string
            params: Optional parameters for the query
            
        Returns:
            Dictionary representing the single result, or None if no results
        """
        results = self.execute_query(query, params)
        return results[0] if results else None
    
    def test_connection(self) -> bool:
        """
        Test the database connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                return result is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

# Global instance
db = SnowflakeConnection()