import pandas as pd
from tabulate import tabulate
from consolemenu import *
from consolemenu.items import *

class ReadWatchList:
    def __init__(self):
        self.file_path = "read-watchlist.xlsx"
        self.data = pd.DataFrame()
        self.menu = ConsoleMenu("Read-WatchList", "Welcome to the Read-WatchList!")
        self.load_data()
        self.create_menu()

    def load_data(self):
        self.data = pd.read_excel(self.file_path, index_col=0)
    
    def save_data(self):
        self.data.to_excel(self.file_path, index=True)
        input("\nSave To File Successful! Press Any Key to Continue")

    def view_data(self):
        print(tabulate(self.data, headers='keys', tablefmt='psql'))
        input("\nPress Any Key to Continue")
    
    def add_entry(self):
        new_entry = {
            'name': input("Enter the name of the entry: "),
            'type': input("Enter the type of the entry (Anime | Manga | Manhwa | Manhua | Novel ): "),
            'bookmark': input("Enter the bookmark for the entry: "),
            'work_status': input("Enter the work status for the entry (Coming Soon | Ongoing | Dropped | Completed): "),
            'my_status': input("Enter your status for the entry (To Do | In Progress | Dropped | Done): "),
            'year_created': input("Enter the year created: "),
            'year_finished': input("Enter the year finished (if applicable): ")
        }

        for key, value in new_entry.items():
            if not value: 
                new_entry[key] = float('nan')

        new_entry_df = pd.DataFrame(new_entry, index=[0])
        self.data = pd.concat([self.data, new_entry_df], ignore_index=True)
        input("\nAdd Entry Successful! Press Any Key to Continue")

    def update_entry(self):
        self.view_data()
        while True:
            update_index = int(input("\nWhat row would you like to update?: "))
            if 0 <= update_index < len(self.data):
                break
            else:
                print("Invalid row. Please enter a valid row")

        print("Columns:")
        for row_id, col in enumerate(self.data.columns):
            print(f"{row_id}: {col}")

        while True:
            update_column_index = input("\nWhich column would you like to update?: ")
            if update_column_index.isdigit() and 0 <= int(update_column_index) < len(self.data.columns):
                break
            else:
                print("Invalid Column. Choose a valid column number.")

        update_column = self.data.columns[int(update_column_index)]
        new_value = input("Enter the new value: ")
        self.data.iloc[update_index, self.data.columns.get_loc(update_column)] = new_value
        input("Update Entry Successful! Press Any Key to Continue")


    def delete_entry(self):
        self.view_data()
        while True:
            delete_index = int(input("\nWhat row would you like to delete?: "))
            if 0 <= delete_index < len(self.data):
                break
                
            else:
                print("Invalid row. Please enter a valid row.")
        self.data = self.data.drop(delete_index)
        self.data.reset_index(drop=True, inplace=True)
        print("Entry deleted successfully.")
        input("\nPress any key to continue")

    def create_menu(self):
        function_items = [
            FunctionItem("View Entries", self.view_data),
            FunctionItem("Add an Entry", self.add_entry),
            FunctionItem("Update an Entry", self.update_entry),
            FunctionItem("Delete an Entry", self.delete_entry),
            FunctionItem("Save To File", self.save_data)
        ]
        for item in function_items:
            self.menu.append_item(item)

    def run(self):
        self.menu.show()

if __name__ == "__main__":
    my_list = ReadWatchList()
    my_list.run()