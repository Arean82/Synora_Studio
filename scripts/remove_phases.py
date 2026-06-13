# scripts/remove_phases.py
# Module containing functions: main.

import os
import glob
import re

def main():
    print("Scanning for 'Phase' notations...")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    py_files = glob.glob(os.path.join(project_root, '**', '*.py'), recursive=True)
    
    # Matches "", "", "" etc.
    pattern = re.compile(r'\s*\]*\)', re.IGNORECASE)
    count = 0
    
    for py_file in py_files:
        if any(ignore in py_file for ignore in ['.venv', 'venv', '__pycache__', '.git', '.tox']):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            continue
            
        # Perform regex replacement
        new_content, num_replacements = pattern.subn('', content)
        
        if num_replacements > 0:
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Print relative path nicely
            rel_path = os.path.relpath(py_file, project_root).replace('\\', '/')
            print(f"Removed {num_replacements} 'Phase' notation(s) from {rel_path}")
            count += 1
            
    print(f"\nSuccessfully cleaned 'Phase' notations from {count} files.")

if __name__ == "__main__":
    main()
