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
        # parameters
        self.date = date
        self.description = description
        self.exp_type = exp_type
        self.exp_curr = currency
        self.exp_amt = amount
        # toplevel frames
        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.pack(expand=True, fill=ctk.BOTH)
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(expand=True, fill=ctk.BOTH)
        # toplevel widgets
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


class QueryToplevel(ctk.CTkToplevel):

    def __init__(self):
        # window
        super().__init__(self)
        self.geometry('300x150')
        self.title('Queries & Reports')
        # vals & vars
        self.measure_vals = ['total', 'percent']
        self.measure_var = ctk.StringVar()
        self.type_var = ctk.StringVar()
        self.compare_var = ctk.IntVar()
        self.output_var = ctk.IntVar()
        # frames
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(expand=True, fill=ctk.BOTH)
        self.compare_frame = ctk.CTkFrame(self)
        self.compare_frame.pack(expand=True, fill=ctk.BOTH)
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(expand=True, fill=ctk.BOTH)
        # row 1 widgets
        self.type_query_lbl = ctk.CTkLabel(self.entry_frame, text="Expense type", font=LABEL_FONT)
        self.type_query_lbl.grid(row=0, column=0, sticky=ctk.NSEW)
        self.type_query_box = ctk.CTkComboBox(self.entry_frame, values=EXPENSE_TYPES, variable=self.type_var)
        self.type_query_box.grid(row=1, column=0, sticky=ctk.NSEW)
        self.measure_box_lbl = ctk.CTkLabel(self.entry_frame, text="Metric", font=LABEL_FONT)
        self.measure_box_lbl.grid(row=0, column=1, sticky=ctk.NSEW, font=LABEL_FONT)
        self.measure_box = ctk.CTkComboBox(self.entry_frame, values=self.measure_vals, variable=self.measure_var)
        self.measure_box.grid(row=1, column=1, sticky=ctk.NSEW)
        self.from_date_lbl = ctk.CTkLabel(self.entry_frame, text="From date", font=LABEL_FONT)
        self.from_date_lbl.grid(row=0, column=2, sticky=ctk.NSEW)
        self.from_date = DateEntry(self.entry_frame, font=DATE_ENTRY_FONT)
        self.from_date.grid(row=1, column=2, sticky=ctk.NSEW)
        self.to_date_lbl = ctk.CTkLabel(self.entry_frame, text="To date", font=LABEL_FONT)
        self.to_date_lbl.grid(row=0, column=3)
        self.to_date = DateEntry(self.entry_frame, font=DATE_ENTRY_FONT)
        # row 2 widgets
        self.radio_btn_lbl = ctk.CTkLabel(self.compare_frame, text="Compare with a different time period")
        self.radio_btn_lbl.grid(row=0, column=0, sticky=ctk.NSEW)
        self.no_radio_btn = ctk.CTkRadioButton(self.compare_frame, text="No", variable=self.compare_var, value=0)
        self.no_radio_btn.grid(row=0, column=1, sticky=ctk.NSEW)
        self.yes_radio_btn = ctk.CTkRadioButton(self.compare_frame, text="Yes", variable=self.compare_var, value=1)
        self.yes_radio_btn.grid(row=0, column=2, sticky=ctk.NSEW)
        self.compare_from_date = DateEntry(self.compare_frame, font=DATE_ENTRY_FONT)
        self.compare_from_date.grid(row=0, column=3, sticky=ctk.NSEW)
        self.compare_to_date = DateEntry(self.compare_frame, font=DATE_ENTRY_FONT)
        self.compare_to_date.grid(row=0, column=4, sticky=ctk.NSEW)
        # row 3 widgets
        self.output_lbl = ctk.CTkLabel(self.btn_frame, text="Output format", font=LABEL_FONT)
        self.output_lbl.grid(row=0, column=0, sticky=ctk.NSEW)
        self.pdf_radio_btn = ctk.CTkRadioButton(self.btn_frame, text="PDF", variable=self.output_var, value=0)
        self.pdf_radio_btn.grid(row=0, column=1, sticky=ctk.NSEW)
        self.spd_sht_btn = ctk.CTkRadioButton(self.btn_frame, text="XLS", variable=self.output_var, value=1)
        self.spd_sht_btn.grid(row=0, column=1, sticky=ctk.NSEW)
        self.execute_btn = ctk.CTkButton(self.btn_frame, text="Execute query", font=BUTTON_FONT)
        self.execute_btn.grid(row=0, column=2, sticky=ctk.NSEW)

