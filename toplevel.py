import customtkinter as ctk
from constants import *


class SaveToplevel(ctk.CTkToplevel):

    def __init__(self, date, description, exp_type, currency, amount):
        # Window
        ctk.CTkToplevel.__init__(self)
        self.geometry('300x150')
        self.title('Save Expense')
        self.wm_transient()
        # parameters
        self.date = date
        self.description = description
        self.exp_type = exp_type
        self.currency = currency
        self.amount = amount
        # toplevel frames
        label_frame = ctk.CTkFrame(self)
        label_frame.pack(expand=True, fill=ctk.BOTH)
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(expand=True, fill=ctk.BOTH)
        # toplevel widgets
        tl_date = ctk.CTkLabel(label_frame, anchor='center', justify=ctk.CENTER, text=f"Date: {date}",
                               font=LABEL_FONT)
        tl_date.pack()
        tl_exp_desc = ctk.CTkLabel(label_frame, text=f"Description: {description}",
                                   font=LABEL_FONT, wraplength=380, padx=10)
        # tl_exp_desc.grid(row=1, column=0)
        tl_exp_desc.pack(expand=True, fill=ctk.BOTH)
        tl_exp_type = ctk.CTkLabel(label_frame, padx=10, text=f"Expense type: {exp_type}",
                                   font=LABEL_FONT)
        tl_exp_type.pack(expand=True, fill=ctk.BOTH)
        # tl_exp_type.grid(row=2, column=0)
        tl_exp_amt = ctk.CTkLabel(label_frame, text=f"Amount: {currency} {amount}",
                                  font=LABEL_FONT)
        tl_exp_amt.pack(expand=True, fill=ctk.BOTH)
        # tl_exp_amt.grid(row=3, column=0)
        tl_btn = ctk.CTkButton(btn_frame, text="Save Expense")
        tl_btn.pack(expand=True, fill=ctk.BOTH)
        # tl_btn.configure(command=lambda: (self.get_expense_info(), self.convert_to_usd(), self.destroy()))

