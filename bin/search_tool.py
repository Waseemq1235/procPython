import tkinter as tk
from tkinter import ttk
from fuzzywuzzy import process
import json
import os

class SearchTool:
    def search(self):
        query = self.entry.get()
        self.results.delete('1.0', tk.END)
        
        directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../index'))

        
        if self.json_select.get() == "All":
            all_procs = []
            for json_file in self.available_jsons:
                file_path = os.path.join(directory_path, json_file) 
                # print(f"Attempting to open: {file_path}")  # debug stuff
                with open(file_path, 'r') as file:
                    all_procs.extend(json.load(file))
                procs_to_search = all_procs
        else:
            with open(os.path.join(directory_path, self.json_select.get()), 'r') as file:  # Prepend directory_path to the filename
                procs_to_search = json.load(file)

        if self.search_type.get() == "Fuzzy":
            matches = process.extract(query, [proc['full_path'] for proc in procs_to_search], limit=20)  # Top 20 matches
            for match in matches:
                matched_string = match[0]
                matched_proc = next((proc for proc in procs_to_search if proc['full_path'] == matched_string), None)
                if matched_proc:
                    self.results.insert(tk.END, f"{matched_proc['full_path']}\n")
        else:  # Standard search
            matches = [proc for proc in procs_to_search if query in proc['full_path']]
            displayed_files = set()
            for match in matches:
                if match['file_location'] not in displayed_files:
                    self.results.insert(tk.END, f"\nFile: {match['file_location']}\n")
                    displayed_files.add(match['file_location'])
                self.results.insert(tk.END, f"  {match['full_path']}\n")

    def __init__(self):
        
        # Absolute directory stuff
        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Absolute path stuff
        directory_path = os.path.join(script_directory, '../index')

        # Collect all JSON files in the directory
        self.available_jsons = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.endswith('.json')]

        # Main window
        self.root = tk.Tk()
        self.root.title("Proc Search Tool")
        
        # Entry for search term
        self.entry = ttk.Entry(self.root)
        self.entry.pack(padx=10, pady=10)

        # Drop-down for JSON selection
        self.json_select = ttk.Combobox(self.root, values=self.available_jsons + ["All"])
        self.json_select.set("All")  # Default value
        self.json_select.pack(padx=10, pady=10)
        
        # Drop-down for search type selection
        self.search_type = ttk.Combobox(self.root, values=["Standard", "Fuzzy"])
        self.search_type.set("Standard")  # Default value
        self.search_type.pack(padx=10, pady=10)
        
        # Search Button
        self.button = ttk.Button(self.root, text="Search", command=self.search)
        self.button.pack(padx=10, pady=10)

        # Frame
        self.results_frame = ttk.Frame(self.root)
        self.results_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Text widget
        self.results = tk.Text(self.results_frame, wrap=tk.WORD, width=80, height=30)  # Adjust width and height as desired
        self.results.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.results_frame, command=self.results.yview)
        self.results.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)




    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    tool = SearchTool()
    tool.run()
