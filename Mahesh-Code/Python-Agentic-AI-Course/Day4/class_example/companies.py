class IndianCompany:
    def __init__(self, name, revenue, employees):
        self.name = name
        self.revenue = revenue
        self.employees = employees

    def show_company_details(self):
        print(f"Company Name: {self.name}")
        print(f"Revenue: {self.revenue}")
        print(f"Number of Employees: {self.employees}")    




company1 = IndianCompany("TCS", 1000000, 500000)
company2 = IndianCompany("Reliance", 2000000, 1000000)

company1.show_company_details()
company2.show_company_details()
