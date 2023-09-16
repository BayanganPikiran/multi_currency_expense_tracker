import tkinter as tk
import customtkinter
from constants import *
from tkcalendar import Calendar, DateEntry
# pip install forex-python
from forex_python.converter import CurrencyCodes, CurrencyRates, RatesNotAvailableError
from database import Database
from conversion import Conversion
from toplevel import *
import os

# --------------------------------------------

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk, Conversion):
    def __init__(self):
        super().__init__()
        # Conversion.__init__(self, self.date_var, self.transaction_var, self.curr_var,
        #                     self.curr_amt_var, self.exp_type_var, self.exp_desc_var )
        # Database.__init__(self, "expenses.db")
        # configure window
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.title("Watch Your Dong")
        # Stringvars, Intvars and Vars
        self.date_var = None # We cannot create a DateEntry here and call it in the setup_ui()
        self.transaction_var = tk.IntVar()
        self.currency_amt_var = tk.StringVar()
        self.currency_var = tk.StringVar()
        self.exp_desc_var = tk.StringVar()
        self.exp_type_var = tk.StringVar()
        # date



    def setup_ui(self):
        # create date frame and widgets
        self.date_frame = customtkinter.CTkFrame(self, width=DATE_FRAME_WIDTH, height=DATE_FRAME_HEIGHT)
        self.date_frame.pack(expand=True, fill=tk.BOTH)
        self.date_pick_lbl = customtkinter.CTkLabel(self.date_frame, text='Transaction date:', font=LABEL_FONT)
        self.date_pick_lbl.grid(row=0, column=0, padx=8, pady=5)
        self.date_pick = DateEntry(self.date_frame, font=DATE_ENTRY_FONT)
        self.date_var = self.date_pick.get_date()
        self.date_pick.grid(row=0, column=1, padx=18, pady=5)
        # radio button
        # self.transaction_var = tk.IntVar()
        self.trans_type_btn1 = customtkinter.CTkRadioButton(self.date_frame, text="Deposit",
                                                            variable=self.transaction_var, value=0)
        self.trans_type_btn1.grid(row=0, column=2, padx=10)
        self.trans_type_btn2 = customtkinter.CTkRadioButton(self.date_frame, text="Expense",
                                                            variable=self.transaction_var, value=1)
        self.trans_type_btn2.grid(row=0, column=3, padx=0)
        # deposit frame and widgets
        self.deposit_frame = customtkinter.CTkFrame(self)
        self.deposit_frame.pack(expand=True, fill=tk.BOTH)
        # self.curr_amt_var = tk.StringVar()
        # self.deposit_amt_var = tk.StringVar()
        self.dep_entry_lbl = customtkinter.CTkLabel(self.deposit_frame, text="Deposit amount",
                                                    anchor='w', font=LABEL_FONT)
        self.dep_entry_lbl.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        self.deposit_entry = customtkinter.CTkEntry(self.deposit_frame, placeholder_text="Enter deposit amount here",
                                                    width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                                    textvariable=self.currency_amt_var)
        self.deposit_entry.grid(row=1, column=0, padx=3, pady=3, sticky=tk.NSEW)
        # self.curr_var = tk.StringVar()
        # self.dep_curr_var = tk.StringVar()
        self.dep_curr_lbl = customtkinter.CTkLabel(self.deposit_frame, text="Deposit currency",
                                                   anchor='w', font=LABEL_FONT)
        self.dep_curr_lbl.grid(row=0, column=1, padx=10, sticky=tk.NSEW)
        self.deposit_currency = customtkinter.CTkComboBox(self.deposit_frame, values=CURRENCIES,
                                                          width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                                          variable=self.currency_var)  # !! changed here
        self.deposit_currency.grid(row=1, column=1)

        # expense frame
        self.expense_frame = customtkinter.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=tk.BOTH)
        # expense description
        self.expense_desc_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense description",
                                                       anchor='w', font=LABEL_FONT)
        self.expense_desc_lbl.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        # self.exp_desc_var = tk.StringVar()
        self.exp_desc_entry = customtkinter.CTkEntry(self.expense_frame, placeholder_text="Enter description here",
                                                     width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                                     textvariable=self.exp_desc_var)
        self.exp_desc_entry.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

        # expense type
        self.exp_type_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense type",
                                                   anchor='w', font=LABEL_FONT)
        self.exp_type_lbl.grid(row=0, column=2, sticky=tk.NSEW, padx=10)
        # self.exp_type_var = tk.StringVar()
        self.expense_type = customtkinter.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES,
                                                      width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                                      variable=self.exp_type_var)
        self.expense_type.grid(row=1, column=2)
        # expense exp_amt
        self.expense_amt_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense amount",
                                                      anchor='w', font=LABEL_FONT)
        self.expense_amt_lbl.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=5)
        # self.exp_amt_var = tk.StringVar()
        self.expense_amt_entry = customtkinter.CTkEntry(self.expense_frame,
                                                        placeholder_text="Enter expense exp_amt here",
                                                        width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                                        textvariable=self.currency_amt_var)  # !!changed here
        self.expense_amt_entry.grid(row=3, column=0, columnspan=2, padx=3, pady=3)
        # choose exp_curr for expense
        self.exp_curr_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense currency",
                                                   anchor='w', font=LABEL_FONT)
        self.exp_curr_lbl.grid(row=2, column=2, sticky=tk.NSEW, padx=10, pady=5)
        # self.exp_curr_var = tk.StringVar()
        self.exp_curr = customtkinter.CTkComboBox(self.expense_frame, values=CURRENCIES,
                                                  width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                                  variable=self.currency_var)
        self.exp_curr.grid(row=3, column=2)

        # buttons
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=tk.BOTH)
        self.save_btn = customtkinter.CTkButton(self.button_frame, text="Save Transaction", width=BUTTON_WIDTH,
                                                height=BUTTON_HEIGHT, font=BUTTON_FONT,
                                                command=lambda: self.create_transaction_toplevel())
        self.save_btn.grid(row=2, column=0, padx=3)
        self.query_btn = customtkinter.CTkButton(self.button_frame, text="Query / Update",
                                                 width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=BUTTON_FONT)
        self.query_btn.grid(row=2, column=1, padx=3)


    def create_transaction_toplevel(self):
        transaction_type = self.transaction_var.get()
        if transaction_type == 0:
            self.create_deposit_toplevel()
        elif transaction_type == 1:
            self.create_expense_toplevel()


    # def get_expense_info(self):
    #     print("The following info will later be rolled into a table insert:")
    #     print(f"Date: {self.date_var}")
    #     print(f"Expense exp_amt: {self.exp_curr_var.get()} {self.exp_amt_var.get()}")
    #     print(f"Description: {self.exp_desc_var.get()}")
    #     print(f"Expense type: {self.exp_type_var.get()}")


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

    # def log_expense_decorator(log_file="expense_log.txt"):
    #     def decorator(func):
    #         def wrapper(self, *args, **kwargs):
    #             # Get the relevant information
    #             date = self.date_var
    #             amt = float(self.exp_amt_var.get())
    #             curr = self.exp_curr_var.get()
    #             usd = self.convert_to_usd()
    #             typ = self.exp_type_var.get()
    #             desc = self.exp_desc_var.get()
    #             # Construct the log message
    #             log_message = f"{date}: {curr} {amt}, ${usd}, type: {typ}, description: {desc}"
    #             # Check if the log file exists, if not, create it
    #             if not os.path.exists(log_file):
    #                 with open(log_file, "w") as f:
    #                     f.write("Expense Log\n")
    #             # Append the log message to the log file
    #             with open(log_file, "a") as f:
    #                 f.write(log_message + "\n")
    #             # Call the original function
    #             result = func(self, *args, **kwargs)
    #             return result
    #
    #         return wrapper
    #
    #     return decorator
    #
    # def read_expense_log(self, log_file=None):
    #     if log_file is None:
    #         # Default to a standard location (e.g., project directory)
    #         log_file = "expense_log.txt"
    #
    #     # Full path to the log file (insert your project directory as needed)
    #     log_file_path = os.path.join("/home/boss_andre/Python_Projects/budgeter", log_file)
    #
    #     if not os.path.exists(log_file_path):
    #         return "Expense log file does not exist."
    #
    #     # Check if it's a file, not a directory
    #     if not os.path.isfile(log_file_path):
    #         return "Invalid log file path. It is a directory, not a file."
    #
    #     with open(log_file_path, "r") as f:
    #         content = f.read()
    #
    #     return content

    # @log_expense_decorator()
    # def save_expense(self):
    #
    #     # Get the relevant information
    #     date = self.date_var
    #     exp_amt = float(self.exp_amt_var.get())
    #     exp_curr = self.exp_curr_var.get()
    #     usd = self.convert_to_usd()
    #     exp_typ = self.exp_type_var.get()
    #     exp_desc = self.exp_desc_var.get()
    #
    #     log_message = f"{date}, {exp_curr} {exp_amt}, ${usd}, type: {exp_typ}, description: {exp_desc}"
    #
    #     # Write the log message to the log file
    #     log_file = "expense_log.txt"
    #     with open(log_file, "a") as f:
    #         f.write(log_message + "\n")
    #
    #     # Insert the expense record
    #     self.record_expense(date, exp_amt, exp_curr, usd, exp_typ, exp_desc)
    #     self.get_expense_info()
    #     self.convert_to_usd()
    #     self.confirm_record_input()
    #     print(log_message)
    #     self.destroy()


    def create_deposit_toplevel(self):
        # get parameters for DepositToplevel
        date = self.date_var
        currency = self.currency_var.get()
        amount = self.currency_amt_var.get()
        # create DepositToplevel instance
        dep_toplevel = DepositTopLevel(date, currency, amount)
        save_button = customtkinter.CTkButton(dep_toplevel, text="Save Deposit",
                                              command=lambda: [self.save_expense, self.destroy()])
        save_button.pack(in_=dep_toplevel.button_frame, expand=True, fill=ctk.BOTH)


    def create_expense_toplevel(self):
        # get parameters for ExpenseToplevel
        date = self.date_var
        description = self.exp_desc_var.get()
        exp_type = self.exp_type_var.get()
        currency = self.currency_var.get()
        amount = self.currency_amt_var.get()
        # create ExpenseToplevel instance
        save_toplevel = ExpenseToplevel(date, description, exp_type, currency, amount)

        # create button
        save_button = customtkinter.CTkButton(save_toplevel, text="Save Expense",
                                              command=lambda: [self.save_expense, self.destroy()])
        save_button.pack(in_=save_toplevel.btn_frame, expand=True, fill=ctk.BOTH)


if __name__ == '__main__':
    app = App()
    app.setup_ui()
    app.mainloop()
