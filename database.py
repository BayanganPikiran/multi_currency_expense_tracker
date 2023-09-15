import sqlite3


class Database:

    def __init__(self, db_path):
        self.expenses_db = db_path
        self.conn = sqlite3.connect(self.expenses_db)
        self.cursor = self.conn.cursor()
        self.expense_type_table = self.create_exp_type_table()
        self.expense_record_table = self.create_expense_table()
        self.add_expense_type()

    # ------------------------ Table Creation ---------------------------- #

    def create_exp_type_table(self):
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
            amount DECIMAL(10,2) NOT NULL,            
            usd TEXT NOT NULL, 
            type_fk INTEGER,
            description TEXT,
            FOREIGN KEY(type_fk) REFERENCES Expense_type(type_name));             
        """)
        self.conn.commit()
        return expense_table

    def create_deposit_table(self):
        deposit_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Deposit_record(
            deposit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL, 
            exp_curr TEXT NOT NULL,
            amount DECIMAL (10, 2) NOT NULL,
            usd TEXT NOT NULL)        
        """)
        self.conn.commit()
        return deposit_table

    def create_balance_table(self):
        balance_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Balance_record(
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            starting_balance DECIMAL(10,2) NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('credit', 'debit')),
            transaction_amount DECIMAL(10,2) NOT NULL,
            end_balance DECIMAL(10,2) NOT NULL,
            deposit_id_fk INTEGER,
            expense_id_fk INTEGER,
            FOREIGN KEY(deposit_id_fk) REFERENCES Deposit_record(deposit_id),
            FOREIGN KEY(expense_id_fk) REFERENCES Expense_record(expense_id)
        )""")
        self.conn.commit()
        return balance_table

    # ------------------------ Table Operations ---------------------------- #

    def record_expense(self, date, curr, amt, usd, typ, desc):
        try:
            self.cursor.execute(
                """INSERT INTO Expense_record(date, exp_curr, amount, usd, type_fk, description)
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

    def get_last_expense_id(self):
        try:
            self.cursor.execute("SELECT MAX(expense_id) FROM Expense_record")
            last_expense_id = self.cursor.fetchone()[0]
            if last_expense_id is None:
                return 0  # If no records exist yet
            return last_expense_id
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return 0  # Handle the error gracefully
