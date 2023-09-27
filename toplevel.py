import customtkinter as ctk
from constants import *
from tkcalendar import DateEntry
from tkinter import messagebox
from database import Database


class ExpenseToplevel(ctk.CTkToplevel):

    def __init__(self, date, description, exp_type, currency, amount, usd):
        # Window
        ctk.CTkToplevel.__init__(self)
        self.geometry('300x150')
        self.title('Save Expense')
        self.wm_transient()
        # Attributes
        self.date = date
        self.description = description
        self.exp_type = exp_type
        self.exp_curr = currency
        self.exp_amt = amount
        # Toplevel frames
        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.pack(expand=True, fill=ctk.BOTH)
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(expand=True, fill=ctk.BOTH)
        # Toplevel widgets
        self.save_date = ctk.CTkLabel(self.label_frame, anchor='center', justify=ctk.CENTER, text=f"Date: {date}",
                                      font=LABEL_FONT)
        self.save_date.pack()
        self.save_exp_desc = ctk.CTkLabel(self.label_frame, text=f"Description: {description}",
                                          font=LABEL_FONT, wraplength=380, padx=10)
        self.save_exp_desc.pack(expand=True, fill=ctk.BOTH)
        self.save_exp_type = ctk.CTkLabel(self.label_frame, padx=10, text=f"Expense type: {exp_type}",
                                          font=LABEL_FONT)
        self.save_exp_type.pack(expand=True, fill=ctk.BOTH)
        self.save_exp_amt = ctk.CTkLabel(self.label_frame, text=f"Amount: {currency} {amount}",
                                         font=LABEL_FONT)
        self.save_exp_amt.pack(expand=True, fill=ctk.BOTH)


class QueryTotalToplevel(ctk.CTkToplevel):

    def __init__(self, from_date, to_date, exp_type, total_spent):
        # Window
        ctk.CTkToplevel.__init__(self)
        self.geometry('300x90')
        self.title('Query Results')
        self.wm_transient()
        # Attributes
        self.from_date = from_date
        self.to_date = to_date
        self.exp_type = exp_type
        self.total_spent = total_spent
        # Toplevel frames
        self.date_frame = ctk.CTkFrame(self)
        self.date_frame.pack()
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.pack()
        # Widgets
        self.date_lbl = ctk.CTkLabel(self.date_frame, text=f"Query period: {self.from_date} - {self.to_date}",
                                     font=LABEL_FONT)
        self.date_lbl.pack()
        self.result_lbl = ctk.CTkLabel(self.result_frame,
                                       text=f"A total of ${self.total_spent} was spent on\n"
                                            f" {self.exp_type} during this period",
                                       font=LABEL_FONT)
        self.result_lbl.pack()


class QueryPercentToplevel(ctk.CTkToplevel):

    def __init__(self, from_date, to_date, exp_type, percent_total):
        ctk.CTkToplevel.__init__(self)
        self.geometry('300x90')
        self.title('Query Results')
        self.wm_transient()
        # Attributes
        self.from_date = from_date
        self.to_date = to_date
        self.exp_type = exp_type
        self.percent_total = percent_total
        # Frames
        self.date_frame = ctk.CTkFrame(self)
        self.date_frame.pack()
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.pack()

        # Widgets
        self.date_lbl = ctk.CTkLabel(self.date_frame, text=f"Query period: {self.from_date} - {self.to_date}",
                                     font=LABEL_FONT)
        self.date_lbl.pack()
        self.result_lbl = ctk.CTkLabel(self.result_frame, text=f"The amount spent on {self.exp_type}\n composed "
                                                               f"{self.percent_total} of total\n expenses during this period",
                                       font=LABEL_FONT)
        self.result_lbl.pack()

