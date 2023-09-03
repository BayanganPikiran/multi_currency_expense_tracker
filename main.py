import tkinter as tk
import customtkinter
from constants import *
from tkcalendar import Calendar, DateEntry
from database import Database

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.title("Watch Your Dong")

        # configure grid layout
        # self.grid_rowconfigure(0, weight=0)
        # self.grid_rowconfigure((1, 2, 3), weight=1)

        # create date frame and widgets
        self.date_frame = customtkinter.CTkFrame(self, width=DATE_FRAME_WIDTH, height=DATE_FRAME_HEIGHT)
        self.date_frame.pack(expand=True, fill=tk.BOTH)
        self.date_pick_lbl = customtkinter.CTkLabel(self.date_frame, text='Expense date:', font=LABEL_FONT)
        self.date_pick_lbl.grid(row=0, column=0, padx=8, pady=5)
        self.date_pick = DateEntry(self.date_frame, font=DATE_ENTRY_FONT)
        self.date_pick.grid(row=0, column=1, padx=8, pady=5)

        # expense frame
        self.expense_frame = customtkinter.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=tk.BOTH)
        # expense description
        self.expense_desc_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense description",
                                                       anchor='w', font=LABEL_FONT)
        self.expense_desc_lbl.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        self.exp_desc_entry = customtkinter.CTkEntry(self.expense_frame, placeholder_text="Enter description here",
                                                     width=ENTRY_WIDTH, height=ENTRY_HEIGHT)
        self.exp_desc_entry.grid(row=1, column=0, columnspan=2, padx=3, pady=3)
        # expense type
        self.exp_type_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense type",
                                                   anchor='w', font=LABEL_FONT)
        self.exp_type_lbl.grid(row=0, column=2, sticky=tk.NSEW, padx=10)
        self.expense_type = customtkinter.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES,
                                                      width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT)
        self.expense_type.grid(row=1, column=2)
        # expense amount
        self.expense_amt_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense amount",
                                                      anchor='w', font=LABEL_FONT)
        self.expense_amt_lbl.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=5)
        self.expense_amt_entry = customtkinter.CTkEntry(self.expense_frame,
                                                        placeholder_text="Enter expense amount here",
                                                        width=ENTRY_WIDTH, height=ENTRY_HEIGHT)
        self.expense_amt_entry.grid(row=3, column=0, columnspan=2, padx=3, pady=3)
        # choose currency for expense
        self.currency_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense currency",
                                                   anchor='w', font=LABEL_FONT)
        self.currency_lbl.grid(row=2, column=2, sticky=tk.NSEW, padx=10, pady=5)
        self.currency = customtkinter.CTkComboBox(self.expense_frame, values=CURRENCIES,
                                                  width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT)
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
        self.choose_date()
        self.get_expense_amt()
        self.get_expense_desc()
        self.get_currency()
        self.get_expense_type()

    def choose_date(self):
        chosen_date = self.date_pick.get_date()
        print(chosen_date)
        return chosen_date

    def get_expense_amt(self):
        expense_amt = self.expense_amt_entry.get()
        print(expense_amt)
        return expense_amt

    def get_expense_desc(self):
        expense_desc = self.exp_desc_entry.get()
        print(expense_desc)
        return expense_desc

    def get_currency(self):
        chosen_currency = self.currency.get()
        print(chosen_currency)
        return chosen_currency

    def get_expense_type(self):
        exp_type = self.expense_type.get()
        print(exp_type)
        return exp_type

    def create_save_toplevel(self):
        # toplevel window
        sv_tl = customtkinter.CTkToplevel()
        sv_tl.geometry('200x150')
        sv_tl.title('Save Expense')
        sv_tl.wm_transient(self)
        # toplevel frames
        label_frame = customtkinter.CTkFrame(sv_tl)
        label_frame.pack(expand=True, fill=tk.BOTH)
        btn_frame = customtkinter.CTkFrame(sv_tl)
        btn_frame.pack(expand=True, fill=tk.BOTH)
        # toplevel widgets
        tl_date = customtkinter.CTkLabel(label_frame, anchor='center', justify=tk.CENTER, text=f"Date: {self.choose_date()}",
                                         font=LABEL_FONT)
        tl_date.grid(row=0, column=0)
        tl_exp_desc = customtkinter.CTkLabel(label_frame, text=f"Description: {self.get_expense_desc()}",
                                             font=LABEL_FONT, wraplength=380, padx=10)
        tl_exp_desc.grid(row=1, column=0)
        tl_exp_type = customtkinter.CTkLabel(label_frame, padx=10, text=f"Expense type: {self.get_expense_type()}",
                                             font=LABEL_FONT)
        tl_exp_type.grid(row=2, column=0)
        tl_exp_amt = customtkinter.CTkLabel(label_frame, anchor='w', text=f"Amount: {self.get_currency()} {self.get_expense_amt()}",
                                            font=LABEL_FONT)
        tl_exp_amt.grid(row=3, column=0)
        tl_btn = customtkinter.CTkButton(btn_frame, text="Save Expense",
                                         command=lambda: [self.get_expense_info(), sv_tl.destroy()])
        tl_btn.pack(expand=True, fill=tk.BOTH)


if __name__ == '__main__':
    app = App()
    app.mainloop()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
