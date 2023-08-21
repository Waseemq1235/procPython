# Proc Search and Indexing Tool
This repository provides tools to index and search for specific procs within .dm files. It's beneficial for probably no one, but it's cool.

# 🌟 Features
Fuzzy Searching: Provides an ability to search for procs using fuzzy matching.
Standard Searching: Direct string-based search.
Flexible JSON Integration: Uses JSON files to store and retrieve indexed data. Allows searching across multiple JSONs or a specific one.
GUI: Simple-to-use GUI based on Tkinter.
# 📁 Structure
Indexing Script: Iterates over .dm files in your specified directory, identifying procs and creating a structured JSON index.
Search Tool: A Tkinter GUI application to search the indexed procs either via direct string match or fuzzy matching.
# 🚀 Getting Started
## Prerequisites
Python 3.x
fuzzywuzzy python package:
`pip install fuzzywuzzy`
tkinter: Usually comes bundled with Python standard library.
## Running the Scripts
1. **Indexing:**

First, set the DIRECTORY variable in the indexing script to the folder containing your .dm files. Run the script:

`python indexer.py`

The script will generate JSON files in the ../index directory (or whichever directory you specify as OUTPUT_DIRECTORY).

2. **Search Tool:**

Run:

`python search_tool.py`

You will be presented with a GUI where you can input search queries, choose which JSON files to search through, and decide on the type of search (Standard/Fuzzy).

# 🤝 Contributing
Pull requests are welcome.

# ❗ Issues
If you encounter any issues or have feature requests, file them in the issues section of the repo.
