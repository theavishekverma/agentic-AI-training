import json
import os
from config.logger import get_logger

logger = get_logger('employee_service')

FILE_NAME = "db/employee.json"

class EmployeeService:
    def __init__(self):
        logger.debug("EmployeeService initialized")

    def __repr__(self):
        return f"EmployeeService()"

    def read_employees(self):
        """Read all employee information from the JSON file"""
        logger.debug(f"Reading employees from {FILE_NAME}")
        if not os.path.exists(FILE_NAME):
            logger.warning(f"File {FILE_NAME} does not exist, returning empty list")
            return []
        try:
            with open(FILE_NAME, 'r') as f:
                content = f.read().strip()
                if not content:
                    logger.debug(f"File {FILE_NAME} is empty")
                    return []
                data = json.loads(content)
                logger.debug(f"Successfully read {len(data)} employees from file")
                return data
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Error parsing JSON from {FILE_NAME}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error reading from {FILE_NAME}: {str(e)}")
            return []

    def write_employees(self, employees):
        """Write employee information to the JSON file"""
        try:
            logger.debug(f"Writing {len(employees)} employees to {FILE_NAME}")
            with open(FILE_NAME, 'w') as f:
                json.dump(employees, f, indent=4)
            logger.info(f"Successfully wrote {len(employees)} employees to file")
        except IOError as e:
            logger.error(f"IO error writing to {FILE_NAME}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error writing to {FILE_NAME}: {str(e)}")
            raise    