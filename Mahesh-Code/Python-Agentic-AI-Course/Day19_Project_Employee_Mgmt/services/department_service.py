import json
import os

FILE_NAME = "db/department.json"

class DepartmentService:
    def __init__(self):
        pass

    def __repr__(self):
        return f"DepartmentService()"

    def read_departments(self):
        """Read all departments from the JSON file"""
        if not os.path.exists(FILE_NAME):
            return []
        with open(FILE_NAME, 'r') as f:
            return json.load(f)

    def write_departments(self, departments):
        """Write departments to the JSON file"""
        with open(FILE_NAME, 'w') as f:
            json.dump(departments, f, indent=4)    

