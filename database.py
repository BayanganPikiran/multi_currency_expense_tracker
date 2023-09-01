import sqlite3


class Database:

    def __init__(self, db_path):
        self.expenses_db = db_path
        self.conn = sqlite3.connect(self.expenses_db)
        self.cursor = self.conn.cursor()
        self.expense_category_table = self.create_category_table()
        self.expense_record_table = self.create_expense_table()

    def create_category_table(self):
        category_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_category(
            category_id INTEGER(10) PRIMARY KEY AUTOINCREMENT,
            category_name TEXT(30) NOT NULL);""")
        self.conn.commit()
        return category_table

    def create_expense_table(self):
        expense_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_record(
            expense_id INTEGER(10) PRIMARY KEY AUTOINCREMENT, 
            date TEXT(30) NUT NULL,
            amount DECIMAL(10,2),
            currency TEXT(30), 
            category_fk INTEGER(10),
            description TEXT(200),
            FOREIGN KEY(category_fk) REFERENCES Expense_category(category_id));             
        """)
        self.conn.commit()
        return expense_table

    def record_expense(self, date, amt, curr, ctg, desc):
        self.cursor.execute("INSERT INTO Expense_record(date, amount, currency, category_fk, description)"
                            " VALUES(?, ?, ?, ?, ?)", (date, amt, curr, ctg, desc))
        self.conn.commit()




