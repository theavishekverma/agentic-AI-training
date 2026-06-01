class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance   # private attribute

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
    
    def get_deposited_amount(self):
        return self.__balance
        #return self.__balance

account = BankAccount("Avishek", 1000)
account.deposit(500)

print("\n************** Bank Account Details ****************\n")
print("Account Owner:", account.owner)
print("Deposited Amount: ₹" + str(account.get_deposited_amount()))   # 500
print("Balance in " + account.owner + " account: ₹" + str(account.get_balance()))   # 1500
print("\n****************************************************\n")