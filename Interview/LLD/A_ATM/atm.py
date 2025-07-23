from bank import Bank
from card import Card

class ATM():
    def __init__(self, id: str, location: str, bank: Bank = Bank.Chase, cash: int = 0):
        self.id = id
        self.location = location
        self.bank = bank
        self.cash = cash

    def welcome_screen(self):
        print(f"Welcome to {self.bank.name} ATM at {self.location}.")
        print("Please insert your card to proceed.")

    def check_card(self, card: Card):
        if self.card.is_valid():
            self.pin_screen(card)
        else:
            print("Invalid card! Please try again.")

    def pin_screen(self, card: Card):
        pin = self.get_valid_pin()
        if pin == card.account.pin and self.bank == card.bank:
            try:
                self.transact(card)
            except ValueError:
                print("Please put in a valid amount")

    def transact(self, card):
        transact_type = self.get_valid_transaction_type()
        balance = card.get_balance(transact_type)
        cash_requested = self.get_valid_cash_amount()
        if self.cash >= cash_requested and balance >= cash_requested:
            card.transact(transact_type, cash_requested)
            self.cash -= cash_requested
            print("Thank you for using us")
        else:
            raise ValueError("Requested AMount Exceeded internal values")

    def get_valid_pin() -> int:
        try:
            pin = input("Please Enter a 4-digit Pin: ")
            if not len(pin == 4):
                raise ValueError("Wrong Length for Pin")
            pin = int(pin)
        except:
            raise ValueError("Please only enter numeric numbers")
        
        return pin
