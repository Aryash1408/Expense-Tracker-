class Expense:
    def __init__(self,name,category,amount) -> None:
        self.name=name
        self.category=category
        self.amount=amount

    # when you call repr() on an Expense object, 
    # it will return a string that looks something like 
    # <Expense: Food, Groceries, $50.00>
    # rather retuning address{<expenses.Expense object at 0x000001B73C03F850>} 
    # it will return a string that is upward
    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, Rs{self.amount:.2f}>"
        
        