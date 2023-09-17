import customtkinter
import customtkinter as ctk
from constants import *
from tkcalendar import DateEntry


class ExpenseToplevel(ctk.CTkToplevel):

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
        self.exp_curr = currency
        self.exp_amt = amount
        # toplevel frames
        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.pack(expand=True, fill=ctk.BOTH)
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(expand=True, fill=ctk.BOTH)
        # toplevel widgets
        self.tl_date = ctk.CTkLabel(self.label_frame, anchor='center', justify=ctk.CENTER, text=f"Date: {date}",
                                    font=LABEL_FONT)
        self.tl_date.pack()
        self.tl_exp_desc = ctk.CTkLabel(self.label_frame, text=f"Description: {description}",
                                        font=LABEL_FONT, wraplength=380, padx=10)
        # tl_exp_desc.grid(row=1, column=0)
        self.tl_exp_desc.pack(expand=True, fill=ctk.BOTH)
        tl_exp_type = ctk.CTkLabel(self.label_frame, padx=10, text=f"Expense type: {exp_type}",
                                   font=LABEL_FONT)
        tl_exp_type.pack(expand=True, fill=ctk.BOTH)
        # tl_exp_type.grid(row=2, column=0)
        tl_exp_amt = ctk.CTkLabel(self.label_frame, text=f"Amount: {currency} {amount}",
                                  font=LABEL_FONT)
        tl_exp_amt.pack(expand=True, fill=ctk.BOTH)
        # tl_exp_amt.grid(row=3, column=0)
        # tl_btn = ctk.CTkButton(self.btn_frame, text="Save Expense")
        # tl_btn.pack(expand=True, fill=ctk.BOTH)
        # # tl_btn.configure(command=lambda: (self.get_expense_info(), self.convert_to_usd(), self.destroy()))


class DepositTopLevel(ctk.CTkToplevel):

    def __init__(self, date, currency, amount):
        # window
        ctk.CTkToplevel.__init__(self)
        self.geometry('225x85')
        self.title('Save Deposit')
        self.wm_transient()
        self.configure(background="red")
        # parameters
        self.dep_date = date
        self.dep_curr = currency
        self.dep_amt = amount
        # frame
        self.deposit_frame = ctk.CTkFrame(self)
        self.deposit_frame.pack(expand=True, fill=ctk.BOTH)
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=ctk.BOTH)
        # labels
        self.dep_date_lbl = ctk.CTkLabel(self.deposit_frame, anchor='center', justify=ctk.CENTER,
                                         text=f"Date: {self.dep_date}", font=LABEL_FONT)
        self.dep_date_lbl.pack(expand=True, fill=ctk.BOTH)
        self.dep_statement_lbl = ctk.CTkLabel(self.deposit_frame, text=f"Deposited {self.dep_curr} {self.dep_amt}",
                                              font=LABEL_FONT)
        self.dep_statement_lbl.pack(expand=True, fill=ctk.BOTH)
        self.dep_confirm_btn = ctk.CTkLabel(self.deposit_frame, text="Confirm")
        self.dep_confirm_btn.pack(expand=True, fill=ctk.BOTH)


class StartingBalanceToplevel(ctk.CTkToplevel):
    def __init__(self):
        # window
        ctk.CTkToplevel.__init__(self)
        ctk.set_default_color_theme("green")
        self.geometry("500x150")
        self.title("Starting Balance")
        self.wm_transient()
        self.balance_var = ctk.StringVar()
        # frames
        self.date_frame = ctk.CTkFrame(self, width=DATE_FRAME_WIDTH, height=DATE_FRAME_HEIGHT)
        self.date_frame.pack(expand=True, fill=ctk.BOTH)
        self.entry_frame = ctk.CTkFrame(self)
        self.entry_frame.pack(expand=True, fill=ctk.BOTH)
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=ctk.BOTH)
        # date
        self.start_date = DateEntry(self.date_frame, font=DATE_ENTRY_FONT, width=10)
        self.start_date.grid(row=0, column=1)
        # self.start_date.pack(expand=True, fill=ctk.BOTH)
        # entry
        self.request_balance = ctk.CTkLabel(self.entry_frame, text="Please enter your starting balance",
                                            anchor='w', font=LABEL_FONT)
        self.request_balance.grid(row=0, column=0, padx=10, sticky=ctk.NSEW)
        self.balance_entry = ctk.CTkEntry(self.entry_frame, textvariable=self.balance_var,
                                          width=ENTRY_WIDTH, height=ENTRY_HEIGHT)
        self.balance_entry.grid(row=1, column=0)
        self.balance_curr_lbl = ctk.CTkLabel(self.entry_frame, text="Balance currency", anchor='w', font=LABEL_FONT)
        self.balance_curr_lbl.grid(row=0, column=1)
        self.balance_curr = ctk.CTkComboBox(self.entry_frame, values=CURRENCIES,
                                            width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT)
        self.balance_curr.grid(row=1, column=1)
        # button
        self.save_btn = ctk.CTkButton(self.button_frame, text="Save starting balance", font=BUTTON_FONT)
        self.save_btn.pack(expand=True, fill=ctk.BOTH)
