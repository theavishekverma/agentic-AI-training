import json
import os

FILE_NAME = "db/payroll.json"

class PayrollService:
    def __init__(self):
        pass

    def __repr__(self):
        return f"PayrollService()"

    def read_payroll(self):
        """Read all payroll information from the JSON file"""
        if not os.path.exists(FILE_NAME):
            return []
        with open(FILE_NAME, 'r') as f:
            return json.load(f)

    def write_payroll(self, payroll):
        """Write payroll information to the JSON file"""
        with open(FILE_NAME, 'w') as f:
            json.dump(payroll, f, indent=4)    

