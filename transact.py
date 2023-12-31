from forex_python.converter import CurrencyRates
import os
from database import Database
from datetime import datetime


class ConvertToUSD:
    def __init__(self, base_currency, transaction_amount):
        self.base = base_currency
        self.trans_amt = float(transaction_amount)
        self.c_rates = CurrencyRates()

    def convert_to_usd(self):
        c, b, t = self.c_rates, self.base, self.trans_amt
        ex_rate = c.get_rate(b, 'USD')
        usd_amt = round(t * ex_rate, 2)
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

    def log_expense_decorator(log_file="expense_log.txt"):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                usd = self.convert_to_usd()
                d, b, t = self.date, self.base_curr, self.transaction_amt
                xt, xd = self.exp_type, self.exp_desc
                # Construct the log message
                log_message = f"{d}, Expense: {b} {t}, ${usd}, type: {xt}, description: {xd}"
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

    def read_expense_log(self, log_file="expense_log.txt"):
        if log_file is None:
            log_file = "expense_log.txt"

        log_file_path = os.path.join("/home/boss_andre/Python_Projects/expense_tracker", log_file)

        if not os.path.exists(log_file_path):
            return "Expense log file does not exist."
        if not os.path.isfile(log_file_path):
            return "Invalid log file path. It is a directory, not a file."

        with open(log_file_path, "r") as f:
            content = f.read()
        return content

    @log_expense_decorator()
    def save_expense(self):
        d, b, t = self.date, self.base_curr, self.transaction_amt
        xt, xd = self.exp_type, self.exp_desc
        usd = self.convert_to_usd()

        confirmation_message = f"Expense saved successfully:\n"
        confirmation_message += f"Date: {d}\n"
        confirmation_message += f"Amount: {b} {t}\n"
        confirmation_message += f"Amount in USD: ${usd}\n"
        confirmation_message += f"Expense Type: {xt}\n"
        confirmation_message += f"Description: {xd}"
        print(confirmation_message)

        log_message = f"To be logged: {d}, Expense: {b} {t}, ${usd}, type: {xt}, description: {xd}"
        self.record_expense(d, t, b, usd, xt, xd)
        print(log_message)


class Report(Database):

    def __init__(self, from_date, to_date):
        Database.__init__(self, "expenses.db")
        self.from_date = from_date
        self.to_date = to_date
        self.reports_dir = self.create_main_reports_dir()

    def create_main_reports_dir(self):
        path = './expense_reports'
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def create_new_report_dir(self):
        f_date = self.from_date
        t_date = self.to_date
        path = self.reports_dir
        new_dir = f"{path}/expense_report_{f_date}_to_{t_date}"
        os.makedirs(new_dir, exist_ok=True)
        return new_dir

    def create_report_csv(self):
        f_date = self.from_date
        t_date = self.to_date
        report_dir = self.create_new_report_dir()
        csv_filename = f"report_csv_{f_date}_to_{t_date}.csv"
        self.generate_report_csv(f_date, t_date, os.path.join(report_dir, csv_filename))

    def create_report_log(self):
        f_date = self.from_date
        t_date = self.to_date
        report_dir = self.create_new_report_dir()
        expense_log_filename = 'expense_log.txt'

        expense_log_report = []
        with open(expense_log_filename, 'r') as log_file:
            for line in log_file:
                parts = line.split(',')
                if len(parts) >= 1:
                    entry_date_str = parts[0].strip()
                    try:
                        # Modify date parsing to match the "YYYY-MM-DD" format
                        entry_date = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                        if f_date <= entry_date <= t_date:
                            expense_log_report.append(line)
                    except ValueError:
                        pass

        # Write expense log report
        report_log_filename = f"report_log_{f_date}_to_{t_date}.txt"
        with open(os.path.join(report_dir, report_log_filename), 'w') as report_file:
            report_file.writelines(expense_log_report)

        print(f"Expense reports generated and copied to the directory: {report_dir}")
