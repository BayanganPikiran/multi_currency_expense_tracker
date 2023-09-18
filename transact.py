from forex_python.converter import CurrencyCodes, CurrencyRates, RatesNotAvailableError
import os
from database import Database
from icecream import ic


class ConvertToUSD:
    def __init__(self, base_currency, transaction_amount):
        self.base = base_currency
        self.trans_amt = float(transaction_amount)
        self.c_rates = CurrencyRates()

    def convert_to_usd(self):
        c, b, t = self.c_rates, self.base, self.trans_amt
        ic(c.get_rates('USD'))
        ic(b)
        ex_rate = c.get_rate(b, 'USD')
        usd_amt = round(t * ex_rate, 2)
        ic(usd_amt)
        return usd_amt


class SaveTransaction(Database, ConvertToUSD):

    def __init__(self, date, trans_type, base_curr, amt_curr, exp_type, exp_desc):
        Database.__init__(self, "expenses.db")
        ConvertToUSD.__init__(self, base_curr, amt_curr)
        self.date = date
        self.transaction_type = trans_type  # Add this line
        self.base_curr = base_curr
        self.transaction_amt = amt_curr
        self.exp_type = exp_type
        self.exp_desc = exp_desc

    def log_transaction_decorator(log_file="expense_log.txt"):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                usd = self.convert_to_usd()
                d, b, t = self.date, self.base_curr, self.transaction_amt
                xt, xd = self.exp_type, self.exp_desc
                # Construct the log message
                if self.transaction_type == 0:
                    log_message = f"{d}, Deposit: {b} {t}, ${usd}"
                    ic(log_message)
                elif self.transaction_type == 1:
                    log_message = f"{d}, Expense: {b} {t}, ${usd}, type: {xt}, description: {xd}"
                    ic(log_message)
                # log_message = f"{date}: {curr} {amt}, ${usd}, type: {typ}, description: {desc}"
                # Check if the log file exists, if not, create it
                if not os.path.exists(log_file):
                    with open(log_file, "w") as f:
                        f.write("Expense Log\n")
                # Append the log message to the log file
                with open(log_file, "a") as f:
                    f.write(log_message + "\n")

                # Call the original function
                result = func(self, *args, **kwargs)
                return result

            return wrapper

        return decorator  # Return the decorator function, don't call it here

    def read_expense_log(self, log_file=None):
        if log_file is None:
            # Default to a standard location (e.g., project directory)
            log_file = "expense_log.txt"

        # Full path to the log file (insert your project directory as needed)
        log_file_path = os.path.join("/home/boss_andre/Python_Projects/budgeter", log_file)

        if not os.path.exists(log_file_path):
            return "Expense log file does not exist."

        # Check if it's a file, not a directory
        if not os.path.isfile(log_file_path):
            return "Invalid log file path. It is a directory, not a file."

        with open(log_file_path, "r") as f:
            content = f.read()

        return content

    @log_transaction_decorator()
    def save_expense(self):
        d, b, t = self.date, self.base_curr, self.transaction_amt
        xt, xd = self.exp_type, self.exp_desc
        usd = self.convert_to_usd()

        # Construct a confirmation message
        confirmation_message = f"Expense saved successfully:\n"
        confirmation_message += f"Date: {d}\n"
        confirmation_message += f"Amount: {b} {t}\n"
        confirmation_message += f"Amount in USD: ${usd}\n"
        confirmation_message += f"Expense Type: {xt}\n"
        confirmation_message += f"Description: {xd}"

        # Print the confirmation message
        print(confirmation_message)

        # Create a log message
        log_message = f"To be logged: {d}, Expense: {b} {t}, ${usd}, type: {xt}, description: {xd}"

        # Log the message (the decorator will handle creating the log file)
        ic(log_message)

        # Insert the expense record
        self.record_expense(d, t, b, usd, xt, xd)

        # Confirm the record input
        self.confirm_record_input()

        # Print the log message
        print(log_message)
