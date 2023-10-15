This is an expense tracking device built with Python, Sqlite3 and customtkinter.  It is entitled "Rawatkan Rupuiahnya", meaning
"Look After Your Rupiah" in Bahasa Indonesia.  This is reflective of the country where I reside at the time of this program's 
creation.  The rupiah is the national currency of Indonesia.

This app performs three core tasks:
1. Records expenses
2. Queries expenses
3. Generates expense reports

At the top of the app is a DateEntry defaulted to the current date.  This date is passed into expenses, which are 
recorded with the following parameters:

* Expense description - An entry for recording the specific expense information
* Expense type - Combobox; there is a list of expense types in the constants.py file that are passed into the combobox values.
* Expense amount - An entry that takes in the nominal amount of the currency being used for the transaction.
* Expense currency - Combobox; the free forex_python library was used.  From this the available Southeast Asian currencies, as well as USD, were passed in as values.

When 'Save Transaction' is clicked, a toplevel returns the aforementioned input.  The save button of said toplevel
confirms the expense, converts the expense amount to USD, and inserts the expense in both the native currency and USD
to the Expense_record table.  At the same time, the expense is logged in expense_log.txt.

Queries can be performed for unique expense types over a selected time period, stipulated via the 'Date from' and 'Date to' Date Entries 
below the 'Expense Currency' combobox, or for the total expense over a selected time period. Furthermore, the query metric can either for the total currency amount attributable to the chosen expense type, or for the percentage
of the total expense that the chosen expense type accounted for.  These queries are measured in USD, allowing for expenses to be incurred 
in multiple countries over a queried time period.

It's important to note that expense and query radio buttons are situated in the top right corner of the app.  In order save an expense 
or perform a query, their respective radio button must be selected.  If it is not, the user will receive a notification in 
a message box alerting them to said requirement.

Finally, users can generate reports on total expenses over a chosen time period, using the same Date Entries applied in queries.
Reports are returned in unique directories, and contain the following:

1. A csv spreadsheet which lists all the expense types, their respective USD amounts, and percentage of total USD for the chosen period.
2. A report_log of all the expense logs recorded in the chosen period.

In the future, this app could be expanded upon in a number of ways.  For instance:

* A ledger could be included to record all deposits and keep track of cash-on-hand at any given time.
* Adding a budgetary constraint feature with which one could set set and achieve budgetary goals over set time intervals.
* Update options for editing recorded expenses, or adding expense types and currencies.
* Additional query and report functionality to compare expense metrics between different time periods, e.g. % spent on an expense type in period A vs period B
* Automation whereby the app is automatically run at a given time to remind users to record their expenses, or to produce automated reports at given time intervals.

If you have any suggestions or feedback on my code, please don't hesitate to contact me.

Live long and prosper.

