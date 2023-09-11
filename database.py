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
            category_id integer PRIMARY KEY AUTOINCREMENT,
            category_name text NOT NULL UNIQUE)""")
        self.conn.commit()
        return category_table

    # accounts_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
    #             id integer PRIMARY KEY AUTOINCREMENT,
    #             website text NOT NULL,
    #             username text NOT NULL,
    #             password text,
    #             UNIQUE(website, username))""")

    def create_expense_table(self):
        expense_table = self.cursor.execute("""CREATE TABLE IF NOT EXISTS Expense_record(
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            currency TEXT NOT NULL, 
            category_fk INTEGER,
            description TEXT,
            FOREIGN KEY(category_fk) REFERENCES Expense_category(category_id));             
        """)
        self.conn.commit()
        return expense_table

    def record_expense(self, date, amt, curr, usd, ctg, desc):
        self.cursor.execute("INSERT INTO Expense_record(date, amount, currency, usd, category_fk, description)"
                            " VALUES(?, ?, ?, ?, ?)", (date, amt, curr, usd, ctg, desc))
        self.conn.commit()

    def add_expense_category(self, new_category=None):
        # List of categories to be added
        categories_to_add = [
            'electricity', 'entertainment', 'fruit', 'groceries', 'health', 'household_items',
            'internet', 'misc', 'petrol', 'rent', 'restaurant', 'supplements',  'travel',
            'visas',
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
