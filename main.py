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
import tkinter.messagebox as messagebox
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
        self.btn_var = ctk.IntVar()
        self.deposit_amt_var = ctk.StringVar()
        self.expense_amt_var = ctk.StringVar()
        self.deposit_curr_var = ctk.StringVar()
        self.expense_curr_var = ctk.StringVar()
        self.exp_desc_var = ctk.StringVar()
        self.exp_type_var = ctk.StringVar()
        self.query_var = ctk.StringVar()
        self.query_metric_var = ctk.StringVar()

    def setup_ui(self):
        # create date frame and widgets
        self.date_frame = ctk.CTkFrame(self, width=DATE_FRAME_WIDTH, height=DATE_FRAME_HEIGHT)
        self.date_frame.pack(expand=True, fill=ctk.BOTH)
        self.date_pick_lbl = ctk.CTkLabel(self.date_frame, text='Transaction date:', font=LABEL_FONT)
        self.date_pick_lbl.grid(row=0, column=0, padx=8, pady=5)
        self.date_pick = DateEntry(self.date_frame, font=DATE_ENTRY_FONT)
        self.date_var = self.date_pick.get_date()
        self.date_pick.grid(row=0, column=1, padx=18, pady=5)
        # radio buttons
        self.expense_button = ctk.CTkRadioButton(self.date_frame, text="Expense", variable=self.btn_var, value=0)
        self.expense_button.grid(row=0, column=2, padx=15, pady=5)
        self.query_button = ctk.CTkRadioButton(self.date_frame, text="Query", variable=self.btn_var, value=1)
        self.query_button.grid(row=0, column=3, pady=5)

        # expense frame
        self.expense_frame = ctk.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=ctk.BOTH)

        # expense description
        self.expense_desc_lbl = ctk.CTkLabel(self.expense_frame, text="Expense description",
                                             anchor='w', font=LABEL_FONT)
        self.expense_desc_lbl.grid(row=0, column=0, padx=10, sticky=ctk.NSEW)
        self.exp_desc_entry = ctk.CTkEntry(self.expense_frame, placeholder_text="Enter description here",
                                           width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                           textvariable=self.exp_desc_var)
        self.exp_desc_entry.grid(row=1, column=0, padx=3, pady=3)

        # expense type
        self.exp_type_lbl = ctk.CTkLabel(self.expense_frame, text="Expense type",
                                         anchor='w', font=LABEL_FONT)
        self.exp_type_lbl.grid(row=0, column=2, sticky=ctk.NSEW, padx=10)
        self.expense_type = ctk.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES,
                                            width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                            variable=self.exp_type_var)
        self.expense_type.grid(row=1, column=2)

        # expense exp_amt
        self.expense_amt_lbl = ctk.CTkLabel(self.expense_frame, text="Expense amount",
                                            anchor='w', font=LABEL_FONT)
        self.expense_amt_lbl.grid(row=2, column=0, sticky=ctk.NSEW, padx=10)
        self.expense_amt_entry = ctk.CTkEntry(self.expense_frame,
                                              placeholder_text="Enter expense exp_amt here",
                                              width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                              textvariable=self.expense_amt_var)  # !!changed here
        self.expense_amt_entry.grid(row=3, column=0, padx=3, pady=3)

        # choose exp_curr for expense
        self.exp_curr_lbl = ctk.CTkLabel(self.expense_frame, text="Expense currency",
                                         anchor='w', font=LABEL_FONT)
        self.exp_curr_lbl.grid(row=2, column=2, sticky=ctk.NSEW, padx=10)
        self.exp_curr = ctk.CTkComboBox(self.expense_frame, values=CURRENCIES,
                                        width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                        variable=self.expense_curr_var)
        self.exp_curr.grid(row=3, column=2)

        # query frame
        self.query_frame = ctk.CTkFrame(self)
        self.query_frame.pack(expand=True, fill=ctk.BOTH)

        # query widgets
        self.type_to_query_lbl = ctk.CTkLabel(self.query_frame, text="Query", anchor='w', font=LABEL_FONT)
        self.type_to_query_lbl.grid(row=0, column=0, padx=10, sticky=ctk.NSEW)
        self.type_to_query = ctk.CTkComboBox(self.query_frame, width=152, height=ENTRY_HEIGHT,
                                             values=EXPENSE_QUERY_TYPES, variable=self.query_var)
        self.type_to_query.grid(row=1, column=0, padx=3, pady=5, sticky=ctk.NSEW)
        self.metric_lbl = ctk.CTkLabel(self.query_frame, text="Metric", anchor='w', font=LABEL_FONT)
        self.metric_lbl.grid(row=0, column=1, padx=10, sticky=ctk.NSEW)
        self.metric_box = ctk.CTkComboBox(self.query_frame, width=152, height=ENTRY_HEIGHT,
                                          values=METRICS, variable=self.query_metric_var)
        self.metric_box.grid(row=1, column=1, padx=3, pady=5, sticky=ctk.NSEW)
        self.date_from_lbl = ctk.CTkLabel(self.query_frame, text="Date from", font=LABEL_FONT)
        self.date_from_lbl.grid(row=0, column=2, padx=10, sticky=ctk.NSEW)
        self.date_from_entry = DateEntry(self.query_frame, width=6, font=DATE_ENTRY_FONT)
        self.date_from_entry.grid(row=1, column=2, padx=10)
        self.date_to_lbl = ctk.CTkLabel(self.query_frame, text="Date to", font=LABEL_FONT)
        self.date_to_lbl.grid(row=0, column=3, padx=10)
        self.date_to_entry = DateEntry(self.query_frame, width=6, font=DATE_ENTRY_FONT)
        self.date_to_entry.grid(row=1, column=3, padx=10)

        # buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=ctk.BOTH)
        self.save_btn = ctk.CTkButton(self.button_frame, text="Save Transaction", width=BUTTON_WIDTH,
                                      height=BUTTON_HEIGHT, font=BUTTON_FONT,
                                      command=lambda: self.create_expense_toplevel())
        self.save_btn.grid(row=2, column=0, padx=3)
        self.run_query_btn = ctk.CTkButton(self.button_frame, text="Query / Update",
                                           width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=BUTTON_FONT,
                                           command=lambda: self.create_query_toplevel())
        self.run_query_btn.grid(row=2, column=1, padx=3)

    def route_query(self):
        if self.btn_var == 1:
            if self.query_metric_var == 'percent':
                self.query_percent()
            elif self.query_metric_var == 'total':
                self.query_total()
        elif self.btn_var == 0:
            messagebox.showerror("Incorrect Operation Type", """You chose to record an expense but are
             trying to query.  Please choose the correct radiobutton to continue""")

    def query_percent(self):
        pass

    def query_total(self):
        pass

    def get_expense_info(self):
        print("The following info will later be rolled into a table insert:")
        print(f"Date: {self.date_var}")
        print(f"Expense, {self.date_var},expense amount: {self.expense_curr_var.get()} {self.expense_amt_var.get()}")
        print(f"Expense description: {self.exp_desc_var.get()}, expense type: {self.exp_type_var.get()}")

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

    # def create_query_toplevel(self):
    #     query = QueryToplevel()
    #     execute_btn = ctk.CTkButton(query, text="Execute query", font=BUTTON_FONT, command=lambda: query.destroy())
    #     execute_btn.grid(in_=query.btn_frame, row=0, column=2, sticky=ctk.NSEW)



if __name__ == '__main__':
    app = App()
    app.setup_ui()
    app.mainloop()
