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

        # create expense frame
        self.expense_frame = customtkinter.CTkFrame(self)
        self.expense_frame.pack(expand=True, fill=tk.BOTH)
        self.exp_desc_entry = customtkinter.CTkEntry(self.expense_frame, placeholder_text="Enter description here")
        self.exp_desc_entry.grid(row=0, column=0, columnspan=2)
        self.expense_type = customtkinter.CTkComboBox(self.expense_frame, values=EXPENSE_TYPES)
        self.expense_type.grid(row=0, column=2)





if __name__ == '__main__':
    app = App()
    app.mainloop()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
