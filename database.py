import sqlite3
from icecream import ic


class Database:

    def __init__(self, db_path):
        self.expenses_db = db_path
        self.conn = sqlite3.connect(self.expenses_db)
        self.cursor = self.conn.cursor()
        self.expense_type_table = self.create_expense_type_table()
        self.expense_record_table = self.create_expense_table()
        self.add_expense_type()

    # ------------------------ Table Creation ---------------------------- #

    def create_expense_type_table(self):
        category_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_type(
            type_id integer PRIMARY KEY AUTOINCREMENT,
            type_name text NOT NULL UNIQUE)""")
        self.conn.commit()
        return category_table

    def create_expense_table(self):
        expense_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_record(
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT NOT NULL,
            exp_curr TEXT NOT NULL,
            exp_amt DECIMAL(10,2) NOT NULL,            
            usd TEXT NOT NULL, 
            type_fk INTEGER,
            description TEXT,
            FOREIGN KEY(type_fk) REFERENCES Expense_type(type_name));             
        """)
        self.conn.commit()
        return expense_table

    # ------------------------ Expense Operations ---------------------------- #

    def add_expense_type(self, new_type=None):
        # List of categories to be added
        types_to_add = [
            'clothing', 'electricity', 'entertainment', 'fruit', 'groceries', 'health', 'household_items',
            'internet', 'misc', 'petrol', 'rent', 'restaurant', 'supplements', 'travel', 'visas',
        ]

        if new_type:
            types_to_add.extend(new_type)
        try:
            for type_name in types_to_add:
                # Check if the category already exists in the table
                self.cursor.execute("SELECT type_name FROM Expense_type WHERE type_name=?",
                                    (type_name,))
                existing_types = self.cursor.fetchone()

                if existing_types is None:
                    # If the category doesn't exist, insert it into the table
                    self.cursor.execute("INSERT INTO Expense_type(type_name) VALUES(?)", (type_name,))
                    print(f"Category '{type_name}' added successfully.")
            self.conn.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)

    def record_expense(self, date, curr, amt, usd, typ, desc):
        try:
            # Record the expense in the Expense_record table
            self.cursor.execute(
                """INSERT INTO Expense_record(date, exp_curr, exp_amt, usd, type_fk, description)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (date, curr, amt, usd, typ, desc)
            )
            self.conn.commit()
            print("Expense record saved successfully.")

        except sqlite3.Error as e:
            print("SQLite error:", e)

    def confirm_record_input(self):
        self.conn = sqlite3.connect(self.expenses_db)
        self.cursor.execute("SELECT * FROM Expense_record")
        print(self.cursor.fetchall())
        self.conn.commit()

    # ------------------------ Expense Query Functions ---------------------------- #

    def calculate_total_expenses_usd(self, expense_type=None, from_date=None, to_date=None):
        try:
            query = """SELECT SUM(usd) FROM Expense_record"""
            params = []

            if expense_type != "all":  # Check if expense_type is not "all"
                query += " WHERE type_fk = (SELECT type_id FROM Expense_type WHERE type_name = ?)"
                params.append(expense_type)

            if from_date and to_date:
                query += " AND date BETWEEN ? AND ?"
                params.extend([from_date, to_date])

            self.cursor.execute(query, params)
            total_usd = self.cursor.fetchone()[0] or 0.0

            return round(total_usd, 2)
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return 0.0

    def calculate_percentage_of_total_usd(self, expense_type=None, from_date=None, to_date=None):
        try:
            total_expenses_usd = self.calculate_total_expenses_usd("all", from_date, to_date)

            if total_expenses_usd > 0:
                # Construct a query to calculate the percentage spent on the chosen expense type
                query = """SELECT SUM(usd) FROM Expense_record"""

                # Add WHERE clause if expense_type is specified and not "all"
                params = []
                if expense_type != "all":
                    query += " WHERE type_fk = (SELECT type_id FROM Expense_type WHERE type_name = ?)"
                    params.append(expense_type)

                # Execute the query with parameters
                self.cursor.execute(query, params)
                total_expense_type_usd = self.cursor.fetchone()[0] or 0.0

                percentage = (total_expense_type_usd / total_expenses_usd) * 100
                return round(percentage, 2)
            else:
                return 0.0
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return 0.0

