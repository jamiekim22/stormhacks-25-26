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

class SecurityAssessmentRepository:
    """Repository class for SecurityAssessment database operations."""
    
    @staticmethod
    def create_security_assessment(assessment_data: dict) -> dict:
        """
        Create a new security assessment in the database.
        
        Args:
            assessment_data: Dictionary containing assessment data
            
        Returns:
            Dictionary with created assessment data including generated ID
            
        Raises:
            DatabaseError: If there's an error creating the assessment
        """
        try:
            # Insert the security assessment
            insert_query = """
                INSERT INTO SecurityAssessments (
                    employee_id, 
                    security_score, 
                    resistance_level, 
                    social_engineering_susceptibility, 
                    feedback, 
                    scoring_explanation
                ) VALUES (%(employee_id)s, %(security_score)s, %(resistance_level)s, %(social_engineering_susceptibility)s, %(feedback)s, %(scoring_explanation)s)
            """
            
            params = {
                'employee_id': assessment_data['employee_id'],
                'security_score': assessment_data['security_score'],
                'resistance_level': assessment_data['resistance_level'],
                'social_engineering_susceptibility': assessment_data['social_engineering_susceptibility'],
                'feedback': assessment_data.get('feedback'),
                'scoring_explanation': assessment_data.get('scoring_explanation')
            }
            
            # Execute the insert
            db.execute_query(insert_query, params)
            
            # Get the created assessment by querying the most recent one for this employee
            select_query = """
                SELECT id, employee_id, assessment_date, security_score, 
                       resistance_level, social_engineering_susceptibility, 
                       feedback, scoring_explanation
                FROM SecurityAssessments 
                WHERE employee_id = %(employee_id)s
                ORDER BY assessment_date DESC 
                LIMIT 1
            """
            
            result = db.execute_query(select_query, {'employee_id': assessment_data['employee_id']})
            
            if not result:
                raise DatabaseError("Failed to retrieve created assessment")
            
            created_assessment = result[0]
            
            # Convert to the expected format
            assessment_response = {
                'id': created_assessment['ID'],
                'employee_id': created_assessment['EMPLOYEE_ID'],
                'assessment_date': str(created_assessment['ASSESSMENT_DATE']),
                'security_score': created_assessment['SECURITY_SCORE'],
                'resistance_level': created_assessment['RESISTANCE_LEVEL'],
                'social_engineering_susceptibility': created_assessment['SOCIAL_ENGINEERING_SUSCEPTIBILITY'],
                'feedback': created_assessment['FEEDBACK'],
                'scoring_explanation': created_assessment['SCORING_EXPLANATION']
            }
            
            logger.info(f"Created security assessment with ID {assessment_response['id']} for employee {assessment_data['employee_id']}")
            return assessment_response
            
        except DatabaseError as e:
            logger.error(f"Database error creating security assessment: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating security assessment: {e}")
            raise DatabaseError(f"Failed to create security assessment: {str(e)}")
    
    @staticmethod
    def get_assessments_by_employee_id(employee_id: int) -> List[dict]:
        """
        Get all security assessments for a specific employee.
        
        Args:
            employee_id: The employee's ID
            
        Returns:
            List of assessment dictionaries
            
        Raises:
            DatabaseError: If there's an error fetching data
        """
        try:
            query = """
                SELECT id, employee_id, assessment_date, security_score, 
                       resistance_level, social_engineering_susceptibility, 
                       feedback, scoring_explanation
                FROM SecurityAssessments 
                WHERE employee_id = %(employee_id)s
                ORDER BY assessment_date DESC
            """
            
            results = db.execute_query(query, {'employee_id': employee_id})
            
            assessments = []
            for row in results:
                assessment = {
                    'id': row['ID'],
                    'employee_id': row['EMPLOYEE_ID'],
                    'assessment_date': str(row['ASSESSMENT_DATE']),
                    'security_score': row['SECURITY_SCORE'],
                    'resistance_level': row['RESISTANCE_LEVEL'],
                    'social_engineering_susceptibility': row['SOCIAL_ENGINEERING_SUSCEPTIBILITY'],
                    'feedback': row['FEEDBACK'],
                    'scoring_explanation': row['SCORING_EXPLANATION']
                }
                assessments.append(assessment)
            
            logger.info(f"Retrieved {len(assessments)} assessments for employee {employee_id}")
            return assessments
            
        except DatabaseError as e:
            logger.error(f"Database error fetching assessments for employee {employee_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching assessments for employee {employee_id}: {e}")
            raise DatabaseError(f"Failed to fetch assessments for employee {employee_id}: {str(e)}")

# Global repository instances
employee_repo = EmployeeRepository()
security_assessment_repo = SecurityAssessmentRepository()