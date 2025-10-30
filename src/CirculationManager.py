#Circulation manager class

class CirculationManager:
    def __init__(self):
        self.is_available = True
        self.due_date = None

    def get_due_date(self):
        return self.due_date

    def is_available(self):
        return self.is_available

    def checkout_book(self, loan_days):
        if self.is_available:
            self.is_available = False
            self.due_date = date.today() + timedelta(days=loan_days)
            return True
        else:
            return False

    def return_book(self):
        if not self.is_available:
            self.is_available = True
            self.due_date = None
