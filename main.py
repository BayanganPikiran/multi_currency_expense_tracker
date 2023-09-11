import tkinter as tk
import requests
import customtkinter
from constants import *
from tkcalendar import Calendar, DateEntry
# pip install forex-python
from forex_python.converter import CurrencyCodes, CurrencyRates, RatesNotAvailableError
from database import Database
from toplevel import *

# --------------------------------------------

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk, SaveToplevel):
    def __init__(self):
        super().__init__()

        # configure window
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.title("Watch Your Dong")
        self.db = Database("expenses.db")
        # self.save_tl = SaveToplevel(self)


        # create date frame and widgets
        self.date_frame = customtkinter.CTkFrame(self, width=DATE_FRAME_WIDTH, height=DATE_FRAME_HEIGHT)
        self.date_frame.pack(expand=True, fill=tk.BOTH)
        self.date_pick_lbl = customtkinter.CTkLabel(self.date_frame, text='Expense date:', font=LABEL_FONT)
        self.date_pick_lbl.grid(row=0, column=0, padx=8, pady=5)
        self.date_pick = DateEntry(self.date_frame, font=DATE_ENTRY_FONT)
        self.date_var = self.date_pick.get_date()
        self.date_pick.grid(row=0, column=1, padx=8, pady=5)

        # expense frame
        self.expense_frame = customtkinter.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=tk.BOTH)
        # expense description
        self.expense_desc_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense description",
                                                       anchor='w', font=LABEL_FONT)
        self.expense_desc_lbl.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        self.exp_desc_var = tk.StringVar()
        self.exp_desc_entry = customtkinter.CTkEntry(self.expense_frame, placeholder_text="Enter description here",
                                                     width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                                     textvariable=self.exp_desc_var)
        self.exp_desc_entry.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

        # expense type
        self.exp_type_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense type",
                                                   anchor='w', font=LABEL_FONT)
        self.exp_type_lbl.grid(row=0, column=2, sticky=tk.NSEW, padx=10)
        self.exp_type_var = tk.StringVar()
        self.expense_type = customtkinter.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES,
                                                      width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT,
                                                      variable=self.exp_type_var)
        self.expense_type.grid(row=1, column=2)
        # expense amount
        self.expense_amt_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense amount",
                                                      anchor='w', font=LABEL_FONT)
        self.expense_amt_lbl.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=5)
        self.exp_amt_var = tk.StringVar()
        self.expense_amt_entry = customtkinter.CTkEntry(self.expense_frame,
                                                        placeholder_text="Enter expense amount here",
                                                        width=ENTRY_WIDTH, height=ENTRY_HEIGHT,
                                                        textvariable=self.exp_amt_var)
        self.expense_amt_entry.grid(row=3, column=0, columnspan=2, padx=3, pady=3)
        # choose currency for expense
        self.currency_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense currency",
                                                   anchor='w', font=LABEL_FONT)
        self.currency_lbl.grid(row=2, column=2, sticky=tk.NSEW, padx=10, pady=5)
        self.curr_var = tk.StringVar()
        self.currency = customtkinter.CTkComboBox(self.expense_frame, values=CURRENCIES,
                                                  width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT, variable=self.curr_var)
        self.currency.grid(row=3, column=2)

        # buttons
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=tk.BOTH)
        self.save_btn = customtkinter.CTkButton(self.button_frame, text="Save Expense", width=BUTTON_WIDTH,
                                                height=BUTTON_HEIGHT, font=BUTTON_FONT,
                                                command=lambda: self.create_save_toplevel())
        self.save_btn.grid(row=2, column=0, padx=3)
        self.query_btn = customtkinter.CTkButton(self.button_frame, text="Create Query",
                                                 width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=BUTTON_FONT)
        self.query_btn.grid(row=2, column=1, padx=3)

    # field functions
    def get_expense_info(self):
        print("The following info will later be rolled into a table insert:")
        print(f"Date: {self.date_var}")
        print(f"Expense amount: {self.curr_var.get()} {self.exp_amt_var.get()}")
        print(f"Description: {self.exp_desc_var.get()}")
        print(f"Expense type: {self.exp_type_var.get()}")

    def convert_to_usd(self):
        base_cur = self.curr_var.get()
        print(base_cur)
        value = float(self.exp_amt_var.get())
        c = CurrencyRates()
        ex_rate = c.get_rate(base_cur, 'USD')
        usd_amt = round(value * ex_rate, 2)
        print(f"${usd_amt}")

    def create_save_toplevel(self):
        # get parameters for SaveToplevel
        date = self.date_var.get()
        description = self.exp_desc_var.get()
        exp_type = self.exp_type_var.get()
        currency = self.curr_var.get()
        amount = self.exp_amt_var.get()
        # create SaveToplevel instance
        save_toplevel = SaveToplevel(date, description, exp_type, currency, amount)
        # create button
        save_button = customtkinter.CTkButton(save_toplevel, text="Save Expense", command=self.save_expense)
        save_button.pack(in_=save_toplevel.btn_frame, expand=True, fill=ctk.BOTH)

    def save_expense(self):
        pass


    # def create_save_toplevel(self):
    #     date = self.date_var
    #     description = self.exp_desc_var.get()
    #     exp_type = self.exp_type_var.get()
    #     amount = self.exp_amt_var.get()
    #     currency = self.curr_var.get()
    #
    #     # toplevel window
    #     sv_tl = customtkinter.CTkToplevel()
    #     sv_tl.geometry('300x150')
    #     sv_tl.title('Save Expense')
    #     sv_tl.wm_transient(self)
    #     # toplevel frames
    #     label_frame = customtkinter.CTkFrame(sv_tl)
    #     label_frame.pack(expand=True, fill=tk.BOTH)
    #     btn_frame = customtkinter.CTkFrame(sv_tl)
    #     btn_frame.pack(expand=True, fill=tk.BOTH)
    #     # toplevel widgets
    #     tl_date = customtkinter.CTkLabel(label_frame, anchor='center', justify=tk.CENTER, text=f"Date: {date}",
    #                                      font=LABEL_FONT)
    #     # tl_date.grid(row=0, column=0)
    #     tl_date.pack()
    #     tl_exp_desc = customtkinter.CTkLabel(label_frame, text=f"Description: {description}",
    #                                          font=LABEL_FONT, wraplength=380, padx=10)
    #     # tl_exp_desc.grid(row=1, column=0)
    #     tl_exp_desc.pack(expand=True, fill=tk.BOTH)
    #     tl_exp_type = customtkinter.CTkLabel(label_frame, padx=10, text=f"Expense type: {exp_type}",
    #                                          font=LABEL_FONT)
    #     tl_exp_type.pack(expand=True, fill=tk.BOTH)
    #     # tl_exp_type.grid(row=2, column=0)
    #     tl_exp_amt = customtkinter.CTkLabel(label_frame, text=f"Amount: {currency} {amount}",
    #                                         font=LABEL_FONT)
    #     tl_exp_amt.pack(expand=True, fill=tk.BOTH)
    #     # tl_exp_amt.grid(row=3, column=0)
    #     tl_btn = customtkinter.CTkButton(btn_frame, text="Save Expense")
    #     tl_btn.pack(expand=True, fill=tk.BOTH)
    #     tl_btn.configure(command=lambda: (self.get_expense_info(), self.convert_to_usd(), sv_tl.destroy()))


if __name__ == '__main__':
    app = App()
    app.mainloop()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
