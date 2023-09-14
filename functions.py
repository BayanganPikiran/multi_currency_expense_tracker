from forex_python.converter import CurrencyCodes, CurrencyRates, RatesNotAvailableError


class Functions:

    def __init__(self, date, base_curr, val_curr, exp_type, exp_desc):
        self.date = date
        self.base_curr = base_curr
        self.curr_val = val_curr
        self.exp_type = exp_type
        self.exp_desc = exp_desc
        self.deposit = False
        self.expense = False

    def get_expense_info(self):
        print("The following info will later be rolled into a table insert:")
        print(f"Date: {self.date}")
        print(f"Expense amount: {self.exp_curr_var.get()} {self.exp_amt_var.get()}")
        print(f"Description: {self.exp_desc_var.get()}")
        print(f"Expense type: {self.exp_type_var.get()}")

    def convert_to_usd(self, base):  # doesn't have all rates
        base_cur = base
        print(base_cur)
        value = float(base_cur)
        c = CurrencyRates()
        print(c.get_rates('USD'))
        ex_rate = c.get_rate(base_cur, 'USD')
        usd_amt = round(value * ex_rate, 2)
        print(f"${usd_amt}")
        return usd_amt

        # def convert_to_usd(self):  # doesn't have all rates
        #     base_cur = self.exp_curr_var.get()
        #     print(base_cur)
        #     value = float(self.exp_amt_var.get())
        #     c = CurrencyRates()
        #     print(c.get_rates('USD'))
        #     ex_rate = c.get_rate(base_cur, 'USD')
        #     usd_amt = round(value * ex_rate, 2)
        #     print(f"${usd_amt}")
        #     return usd_amt

    def log_expense_decorator(log_file="expense_log.txt"):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                # Get the relevant information
                date = self.date_var
                amt = float(self.exp_amt_var.get())
                curr = self.exp_curr_var.get()
                usd = self.convert_to_usd()
                typ = self.exp_type_var.get()
                desc = self.exp_desc_var.get()
                # Construct the log message
                log_message = f"{date}: {curr} {amt}, ${usd}, type: {typ}, description: {desc}"
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

        return decorator

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

    @log_expense_decorator()
    def save_expense(self):
        # Get the relevant information
        date = self.date_var
        exp_amt = float(self.exp_amt_var.get())
        exp_curr = self.exp_curr_var.get()
        usd = self.convert_to_usd()
        exp_typ = self.exp_type_var.get()
        exp_desc = self.exp_desc_var.get()

        log_message = f"{date}, {exp_curr} {exp_amt}, ${usd}, type: {exp_typ}, description: {exp_desc}"

        # Write the log message to the log file
        log_file = "expense_log.txt"
        with open(log_file, "a") as f:
            f.write(log_message + "\n")

        # Insert the expense record
        self.record_expense(date, exp_amt, exp_curr, usd, exp_typ, exp_desc)
        self.get_expense_info()
        self.convert_to_usd()
        self.confirm_record_input()
        print(log_message)
        self.destroy()
