import sqlite3


class Database:

    def __init__(self, db_path):
        self.expenses_db = db_path
        self.conn = sqlite3.connect(self.expenses_db)
        self.cursor = self.conn.cursor()
        self.expense_category_table = self.create_category_table()
        self.expense_record_table = self.create_expense_table()
        self.add_expense_category()


    def create_category_table(self):
        category_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_category(
            category_id INTEGER(10) PRIMARY KEY AUTOINCREMENT,
            category_name TEXT(30) NOT NULL),
            UNIQUE category_name);""")
        self.conn.commit()
        return category_table

    def create_expense_table(self):
        expense_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_record(
            expense_id INTEGER(10) PRIMARY KEY AUTOINCREMENT, 
            date TEXT(30) NUT NULL,
            amount DECIMAL(10,2) NOT NULL,
            currency TEXT(3) NOT NULL, 
            category_fk INTEGER(10),
            description TEXT(200),
            FOREIGN KEY(category_fk) REFERENCES Expense_category(category_id));             
        """)
        self.conn.commit()
        return expense_table

    def record_expense(self, date, amt, curr, ctgy, desc):
        self.cursor.execute("INSERT INTO Expense_record(date, amount, currency, category_fk, description)"
                            " VALUES(?, ?, ?, ?, ?)", (date, amt, curr, ctgy, desc))
        self.conn.commit()

    def add_expense_category(self, new_category=None):
        # List of categories to be added
        categories_to_add = [
            'rent', 'electricity', 'internet', 'groceries', 'restaurant',
            'fruit', 'household_supplies', 'supplements', 'entertainment',
            'petrol', 'travel', 'visas', 'miscellaneous'
        ]

        if new_category:
            categories_to_add.extend(new_category)
        try:
            for category_name in categories_to_add:
                # Check if the category already exists in the table
                self.cursor.execute("SELECT category_id FROM Expense_category WHERE category_name=?",
                                    (category_name,))
                existing_category = self.cursor.fetchone()

                if existing_category is None:
                    # If the category doesn't exist, insert it into the table
                    self.cursor.execute("INSERT INTO Expense_category(category_name) VALUES(?)", category_name)
                    print(f"Category '{category_name}' added successfully.")
            self.conn.commit()
        except sqlite3.Error as e:
            print("SQLite error:", e)
