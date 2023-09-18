import customtkinter as ctk
import tkinter as tk
from constants import *
from tkcalendar import Calendar, DateEntry
# pip install forex-python
from forex_python.converter import CurrencyCodes, CurrencyRates, RatesNotAvailableError
from database import Database
from transact import *
from toplevel import *
from icecream import ic
import os

# --------------------------------------------

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.title("Watch Your Dong")
        # Stringvars, Intvars and Vars
        self.date_var = None  # We cannot create a DateEntry here and call it in the setup_ui()
        self.transaction_var = ctk.IntVar()
        self.deposit_amt_var = ctk.StringVar()
        self.expense_amt_var = ctk.StringVar()
        self.deposit_curr_var = ctk.StringVar()
        self.expense_curr_var = ctk.StringVar()
        self.exp_desc_var = ctk.StringVar()
        self.exp_type_var = ctk.StringVar()

    def setup_ui(self):
        # create date frame and widgets
        self.date_frame = ctk.CTkFrame(self, width=DATE_FRAME_WIDTH, height=DATE_FRAME_HEIGHT)
        self.date_frame.pack(expand=True, fill=ctk.BOTH)
        self.date_pick_lbl = ctk.CTkLabel(self.date_frame, text='Transaction date:', font=LABEL_FONT)
        self.date_pick_lbl.grid(row=0, column=0, padx=8, pady=5)
        self.date_pick = DateEntry(self.date_frame, font=DATE_ENTRY_FONT)
        self.date_var = self.date_pick.get_date()
        self.date_pick.grid(row=0, column=1, padx=18, pady=5)
        # radio button
        self.trans_type_btn1 = ctk.CTkRadioButton(self.date_frame, text="Deposit",
                                                  variable=self.transaction_var, value=0)
        self.trans_type_btn1.grid(row=0, column=2, padx=10)
        self.trans_type_btn2 = ctk.CTkRadioButton(self.date_frame, text="Expense",
                                                  variable=self.transaction_var, value=1)
        self.trans_type_btn2.grid(row=0, column=3, padx=0)
        # deposit frame and widgets
        self.deposit_frame = ctk.CTkFrame(self)
        self.deposit_frame.pack(expand=True, fill=ctk.BOTH)
        self.dep_entry_lbl = ctk.CTkLabel(self.deposit_frame, text="Deposit amount",
                                          anchor='w', font=LABEL_FONT)
        self.dep_entry_lbl.grid(row=0, column=0, padx=10, sticky=ctk.NSEW)
        self.deposit_entry = ctk.CTkEntry(self.deposit_frame, placeholder_text="Enter deposit amount here",
                                          width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                          textvariable=self.deposit_amt_var)
        self.deposit_entry.grid(row=1, column=0, padx=3, pady=3, sticky=ctk.NSEW)
        self.dep_curr_lbl = ctk.CTkLabel(self.deposit_frame, text="Deposit currency",
                                         anchor='w', font=LABEL_FONT)
        self.dep_curr_lbl.grid(row=0, column=1, padx=10, sticky=ctk.NSEW)
        self.deposit_currency = ctk.CTkComboBox(self.deposit_frame, values=CURRENCIES,
                                                width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                                variable=self.deposit_curr_var)  # !! changed here
        self.deposit_currency.grid(row=1, column=1)

        # expense frame
        self.expense_frame = ctk.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=ctk.BOTH)
        # expense description
        self.expense_desc_lbl = ctk.CTkLabel(self.expense_frame, text="Expense description",
                                             anchor='w', font=LABEL_FONT)
        self.expense_desc_lbl.grid(row=0, column=0, padx=10, sticky=ctk.NSEW)
        # self.exp_desc_var = tk.StringVar()
        self.exp_desc_entry = ctk.CTkEntry(self.expense_frame, placeholder_text="Enter description here",
                                           width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                           textvariable=self.exp_desc_var)
        self.exp_desc_entry.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

        # expense type
        self.exp_type_lbl = ctk.CTkLabel(self.expense_frame, text="Expense type",
                                         anchor='w', font=LABEL_FONT)
        self.exp_type_lbl.grid(row=0, column=2, sticky=ctk.NSEW, padx=10)
        # self.exp_type_var = tk.StringVar()
        self.expense_type = ctk.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES,
                                            width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                            variable=self.exp_type_var)
        self.expense_type.grid(row=1, column=2)
        # expense exp_amt
        self.expense_amt_lbl = ctk.CTkLabel(self.expense_frame, text="Expense amount",
                                            anchor='w', font=LABEL_FONT)
        self.expense_amt_lbl.grid(row=2, column=0, sticky=ctk.NSEW, padx=10, pady=5)
        # self.exp_amt_var = tk.StringVar()
        self.expense_amt_entry = ctk.CTkEntry(self.expense_frame,
                                              placeholder_text="Enter expense exp_amt here",
                                              width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                              textvariable=self.expense_amt_var)  # !!changed here
        self.expense_amt_entry.grid(row=3, column=0, columnspan=2, padx=3, pady=3)
        # choose exp_curr for expense
        self.exp_curr_lbl = ctk.CTkLabel(self.expense_frame, text="Expense currency",
                                         anchor='w', font=LABEL_FONT)
        self.exp_curr_lbl.grid(row=2, column=2, sticky=ctk.NSEW, padx=10, pady=5)
        # self.exp_curr_var = tk.StringVar()
        self.exp_curr = ctk.CTkComboBox(self.expense_frame, values=CURRENCIES,
                                        width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                        variable=self.expense_curr_var)
        self.exp_curr.grid(row=3, column=2)

        # buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=ctk.BOTH)
        self.save_btn = ctk.CTkButton(self.button_frame, text="Save Transaction", width=BUTTON_WIDTH,
                                      height=BUTTON_HEIGHT, font=BUTTON_FONT,
                                      command=lambda: self.create_transaction_toplevel())
        self.save_btn.grid(row=2, column=0, padx=3)
        self.query_btn = ctk.CTkButton(self.button_frame, text="Query / Update",
                                       width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=BUTTON_FONT)
        self.query_btn.grid(row=2, column=1, padx=3)



    def create_transaction_toplevel(self):
        transaction_type = self.transaction_var.get()
        if transaction_type == 0:
            ic(transaction_type, "deposit")
            self.create_deposit_toplevel()
        elif transaction_type == 1:
            ic(transaction_type, "expense")
            self.create_expense_toplevel()

    def get_expense_info(self):
        print("The following info will later be rolled into a table insert:")
        print(f"Date: {self.date_var}")
        if self.transaction_var == 0:
            print(f"Deposit, {self.date_var},"
                  f" deposit amount: {self.deposit_curr_var.get()} {self.deposit_amt_var.get()}")
        elif self.transaction_var == 1:
            print(f"Expense, {self.date_var},"
                  f" expense amount: {self.expense_curr_var.get()} {self.expense_amt_var.get()}")
        print(f"Expense description: {self.exp_desc_var.get()}, expense type: {self.exp_type_var.get()}")

    def create_deposit_toplevel(self):
        # get parameters for DepositToplevel
        date = self.date_var
        currency = self.deposit_curr_var.get()
        amount = self.deposit_amt_var.get()
        ic(date, currency, amount)

        # Create an instance of ConvertToUSD
        converter = ConvertToUSD(currency, amount)

        # Calculate the USD amount
        usd_amount = converter.convert_to_usd()

        # create DepositToplevel instance
        dep_toplevel = DepositTopLevel(date, currency, amount, usd_amount)

        save_button = ctk.CTkButton(dep_toplevel, text="Save Deposit",
                                    command=lambda: [self.save_expense(dep_toplevel), dep_toplevel.destroy()])
        save_button.pack(in_=dep_toplevel.button_frame, expand=True, fill=ctk.BOTH)

    def create_expense_toplevel(self):
        # get parameters for ExpenseToplevel
        date = self.date_var
        description = self.exp_desc_var.get()
        exp_type = self.exp_type_var.get()
        currency = self.expense_curr_var.get()
        amount = self.expense_amt_var.get()
        ic(date, description, exp_type, currency, amount)

        # Create an instance of SaveTransaction with the required attributes
        save_transaction = SaveTransaction(date, 1, currency, amount, exp_type, description)

        # Calculate the USD amount using convert_to_usd from SaveTransaction
        usd_amount = save_transaction.convert_to_usd()

        # create ExpenseToplevel instance with the additional usd_amount argument
        save_toplevel = ExpenseToplevel(date, description, exp_type, currency, amount, usd_amount)

        save_button = ctk.CTkButton(save_toplevel, text="Save Expense",
                                    command=lambda: [save_transaction.save_expense(), save_toplevel.destroy()])
        save_button.pack(in_=save_toplevel.btn_frame, expand=True, fill=ctk.BOTH)

        # def create_starting_balance_tl(self):
        #     starting_balance = StartingBalanceToplevel()
        #     save_btn = ctk.CTkButton(starting_balance, text="Save starting balance",
        #                              command=lambda: [self.record_balance_transaction('credit', 0),
        #                                               self.destroy()])
        #     save_btn.pack(in_=starting_balance.button_frame, expand=True, fill=ctk.BOTH)


if __name__ == '__main__':

    app = App()
    app.setup_ui()
    app.mainloop()
