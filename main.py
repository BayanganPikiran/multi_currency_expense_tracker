import tkinter as tk
import customtkinter
from constants import *
from tkcalendar import Calendar, DateEntry

customtkinter.set_appearance_mode("dark")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.title("Watch Your Dong")

        # configure grid layout
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        # create date frame and widgets
        self.date_frame = customtkinter.CTkFrame(self)
        self.date_frame.pack(expand=True, fill=tk.BOTH)
        self.date_pick = DateEntry(self.date_frame)
        self.date_pick.grid(row=0, column=0)

        # expense frame
        self.expense_frame = customtkinter.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=tk.BOTH)

        self.expense_desc_lbl = customtkinter.CTkLabel(self.expense_frame, text="Expense description",
                                                       anchor='w')
        self.expense_desc_lbl.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        self.exp_desc_entry = customtkinter.CTkEntry(self.expense_frame, placeholder_text="Enter description here",
                                                     width=ENTRY_WIDTH, height=ENTRY_HEIGHT)
        self.exp_desc_entry.grid(row=1, column=0, columnspan=2, padx=3, pady=3)

        self.exp_type_lbl = customtkinter.CTkLabel(self.expense_frame, text="Choose expense type", anchor='w')
        self.exp_type_lbl.grid(row=0, column=2, sticky=tk.NSEW, padx=10)
        self.expense_type = customtkinter.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES,
                                                      width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT)
        self.expense_type.grid(row=1, column=2)

        self.expense_amt_lbl = customtkinter.CTkLabel(self.expense_frame, text="Amount expense", anchor='w')
        self.expense_amt_lbl.grid(row=2, column=0, sticky=tk.NSEW, padx=10)
        self.expense_amt_entry = customtkinter.CTkEntry(self.expense_frame, placeholder_text="Enter expense amount here",
                                                        width=ENTRY_WIDTH, height=ENTRY_HEIGHT)
        self.expense_amt_entry.grid(row=3, column=0, columnspan=2, padx=3, pady=3)

        self.currency_lbl = customtkinter.CTkLabel(self.expense_frame, text="Choose currency used", anchor='w')
        self.currency_lbl.grid(row=2, column=2, sticky=tk.NSEW, padx=10)
        self.currency = customtkinter.CTkComboBox(self.expense_frame, values=CURRENCIES,
                                                  width=COMBOBOX_WIDTH, height=COMBOBOX_HEIGHT)
        self.currency.grid(row=3, column=2)

        # buttons
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.pack(expand=True, fill=tk.BOTH)
        self.save_btn = customtkinter.CTkButton(self.button_frame, text="Save Expense", command=print("save expense"))
        self.save_btn.grid(row=2, column=0)
        self.query_btn = customtkinter.CTkButton(self.button_frame, text="Create Query", command=print("Query deez nuts!"))
        self.query_btn.grid(row=2, column=1)





if __name__ == '__main__':
    app = App()
    app.mainloop()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
