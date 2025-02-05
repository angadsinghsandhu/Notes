from bank import Bank
from account import Account

class Card():
    def __init__(self, bank: Bank, account: Account):
        self.bank = bank
        self.account = Account

    def transact()