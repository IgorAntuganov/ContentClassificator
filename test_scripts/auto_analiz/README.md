# Imports auto-analysis (test version)

### Purpose
Visualize the import structure across the project using only built-in Python packages
and DOT language for graph description.  
You may need to use online DOT visualization tools (free) for visualization.  
Script status: mostly working, graph readable, but contains some non-essential information.  
All scripts in the auto_analyze folder were primarily created by AI and slightly enhanced by human  

### Dependencies
Used built-in packages:
- os
- ast
- collections

---

### How to use

1) Text representation:
    - Open `analyze_imports.py` file
    - Specify the correct path to the analyzed folder in the last line of the file
    - Optionally specify EXCLUDED_DIRS at the beginning of the file
    - Run the script and view the total file count, import count, and details in the standard output

2) Graph representation
    - Open `dot_diagram.py` file
    - Specify the correct path to the analyzed folder in the last line of the file
    - Optionally specify EXCLUDED_DIRS at the beginning of the file
    - Run the script and copy the text from the standard output
    - Go to any online DOT visualization tool
    - Paste the copied text and view the result - visualized graph
    - Optionally remove unnecessary text (graph part)

---

### Possible improvements
- Remove unnecessary graph elements
- Add import arrows within packages
- Create a graph for instance usage