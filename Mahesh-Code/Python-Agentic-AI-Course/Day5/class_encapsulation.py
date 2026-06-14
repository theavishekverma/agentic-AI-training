# encapsulation example public and private and protectedattributes
class Employee:
    def __init__(self, name, salary, department,company):
        self.__name = name  # private attribute
        self.__salary = salary  # private attribute
        self._department = department  # protected attribute
        self.company = company  # public attribute
        

    def __get_name(self):
        return self.__name

    def __get_salary(self):
        return self.__salary

    def __get_department(self):
        return self._department
    
    def get_company(self):
        return self.company

    def set_salary(self, salary):
        if salary > 0:
            self.__salary = salary
        else:
            print("Salary must be positive.")


class Manager(Employee):
    def __init__(self, name, salary, department, company, team_size):
        super().__init__(name, salary, department, company)
        self.team_size = team_size  # public attribute

    def get_team_size(self):
        return self.team_size            



mng=Manager("Alice", 50000, "HR", "Te`chCorp",1000)
print(mng._Employee__get_name())
print(mng._Employee__get_salary())
print(mng._Employee__get_department())
print(mng.company)
print(mng.team_size)


'''
emp=Employee("Alice", 50000, "HR", "TechCorp")
print(emp.get_name())  # This will raise an AttributeError because __name is private
emp.set_salary(55000)  # This will work, as set_salary is a public method
print(emp._department)  # This will work, but it's not recommended to access protected attributes
print(emp.company)  # This will work, as company is a public attribute
print(emp.get_salary())  # This will work, as get_salary is a public method
'''

'''
# Example usage
emp1 = Employee("Alice", 50000, "HR", "TechCorp")
print(emp1.get_name())  # Accessing private attribute via getter
print(emp1.get_salary())  # Accessing private attribute via getter
print(emp1.get_department())  # Accessing protected attribute via getter
print(emp1.get_company())  # Accessing public attribute directly
emp1.set_salary(55000)  # Updating salary using setter
print(emp1.get_salary())  # Verifying the updated salary
mgr1 = Manager("Bob", 80000, "IT", "TechCorp", 5)
print(mgr1.get_name())  # Accessing private attribute via getter
print(mgr1.get_team_size())  # Accessing public attribute directly
print(mgr1.get_company())  # Accessing public attribute directly    
'''