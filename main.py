import datetime

class Account:
    def __init__(self, acc_num, acc_type, balance=0.0):
        self.acc_num = acc_num
        self.acc_type = acc_type
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"+${amount} (Deposit)")
        return f"Deposited ${amount}. Balance: ${self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        self.history.append(f"-${amount} (Withdrawal)")
        return f"Withdrew ${amount}. Balance: ${self.balance}"

class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def open_account(self, acc_num, acc_type, init_dep=0.0):
        self.accounts[acc_num] = Account(acc_num, acc_type, init_dep)


user = Customer("Alice")
user.open_account("123", "Savings", 500.0)
active_acc = user.accounts["123"]

print(active_acc.deposit(200))
print(active_acc.withdraw(100))
print("History:", active_acc.history)