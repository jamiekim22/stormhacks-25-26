from typing import List, Optional
import logging
from database import db
from models import Employee
from snowflake.connector.errors import DatabaseError

logger = logging.getLogger(__name__)

class EmployeeRepository:
    """Repository class for Employee database operations."""
    
    @staticmethod
    def get_all_employees() -> List[Employee]:
        """
        Fetch all employees from the database.
        
        Returns:
            List of Employee objects
            
        Raises:
            DatabaseError: If there's an error fetching data
        """
        try:
            query = """
                SELECT id, name, phone_number
                FROM Employees
                WHERE phone_number IS NOT NULL
                ORDER BY name
            """
            
            results = db.execute_query(query)
            
            employees = []
            for row in results:
                # Add a default company name since it's not in the database
                employee_data = {
                    'id': row['ID'],
                    'name': row['NAME'],
                    'phone_number': row['PHONE_NUMBER'],
                    'company': 'Company Name'  # Default company name
                }
                employees.append(Employee(**employee_data))
            
            logger.info(f"Retrieved {len(employees)} employees from database")
            return employees
            
        except DatabaseError as e:
            logger.error(f"Database error fetching employees: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching employees: {e}")
            raise DatabaseError(f"Failed to fetch employees: {str(e)}")
    
    @staticmethod
    def get_employee_by_id(employee_id: int) -> Optional[Employee]:
        """
        Fetch a specific employee by ID.
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            Employee object if found, None otherwise
            
        Raises:
            DatabaseError: If there's an error fetching data
        """
        try:
            query = """
                SELECT id, name, phone_number
                FROM Employees
                WHERE id = %(employee_id)s
                AND phone_number IS NOT NULL
            """
            
            result = db.execute_single_query(query, {'employee_id': employee_id})
            
            if result:
                employee_data = {
                    'id': result['ID'],
                    'name': result['NAME'],
                    'phone_number': result['PHONE_NUMBER'],
                    'company': 'Company Name'  # Default company name
                }
                employee = Employee(**employee_data)
                logger.info(f"Retrieved employee {employee_id}: {employee.name}")
                return employee
            else:
                logger.warning(f"Employee {employee_id} not found")
                return None
                
        except DatabaseError as e:
            logger.error(f"Database error fetching employee {employee_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching employee {employee_id}: {e}")
            raise DatabaseError(f"Failed to fetch employee {employee_id}: {str(e)}")
    
    @staticmethod
    def search_employees(search_term: str) -> List[Employee]:
        """
        Search employees by name or phone number.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching Employee objects
            
        Raises:
            DatabaseError: If there's an error fetching data
        """
        try:
            query = """
                SELECT id, name, phone_number
                FROM Employees
                WHERE (
                    LOWER(name) LIKE LOWER(%(search_term)s)
                    OR phone_number LIKE %(search_term)s
                )
                AND phone_number IS NOT NULL
                ORDER BY name
                LIMIT 100
            """
            
            # Add wildcards for pattern matching
            search_pattern = f"%{search_term}%"
            results = db.execute_query(query, {'search_term': search_pattern})
            
            employees = []
            for row in results:
                employee_data = {
                    'id': row['ID'],
                    'name': row['NAME'],
                    'phone_number': row['PHONE_NUMBER'],
                    'company': 'Company Name'  # Default company name
                }
                employees.append(Employee(**employee_data))
            
            logger.info(f"Search for '{search_term}' returned {len(employees)} employees")
            return employees
            
        except DatabaseError as e:
            logger.error(f"Database error searching employees: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error searching employees: {e}")
            raise DatabaseError(f"Failed to search employees: {str(e)}")
    
    @staticmethod
    def validate_employee_exists(employee_id: int) -> bool:
        """
        Check if an employee exists and has a phone number.
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            True if employee exists with phone number, False otherwise
        """
        try:
            query = """
                SELECT COUNT(*) as count
                FROM Employees
                WHERE id = %(employee_id)s
                AND phone_number IS NOT NULL
            """
            
            result = db.execute_single_query(query, {'employee_id': employee_id})
            exists = result and result['COUNT'] > 0
            
            logger.info(f"Employee {employee_id} existence check: {exists}")
            return exists
            
        except Exception as e:
            logger.error(f"Error validating employee {employee_id}: {e}")
            return False

# Global repository instance
employee_repo = EmployeeRepository()