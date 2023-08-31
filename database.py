import sqlite3


class Database:

    def __init__(self, db_path):
        self.expenses_db = db_path
        self.conn = sqlite3.connect(self.expenses_db)
        self.cursor = self.conn.cursor()
        self.category_table = self.create_category_table()

    def create_category_table(self):
        category_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS expense_category(
            category_id INTEGER(10) PRIMARY KEY AUTOINCREMENT,
            category_name TEXT(30) NOT NULL""")
        self.conn.commit()
        return category_table

    def create_expense_table(self):
        expense_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS expense_record(
            expense_id INTEGER(10) PRIMARY KEY AUTOINCREMENT, 
            date TEXT(30) NUT NULL,
            amount DECIMAL(10,2), 
            category_fk 
        """)
        self.conn.commit()
        return expense_table
    

