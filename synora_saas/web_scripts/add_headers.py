# synora_saas/web_scripts/add_headers.py
# Module containing functions: generate_description, process_file, main.

import os
import ast
import glob

def generate_description(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        
        # 1. Check for module docstring
        docstring = ast.get_docstring(tree)
        if docstring:
            # Use the first line of the docstring, cleaned up
            first_line = docstring.strip().split('\n')[0].strip()
            if first_line:
                return first_line[:150]
            
        # 2. Collect class and function names to auto-generate a description
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')]
        
        desc_parts = []
        if classes:
            desc_parts.append(f"classes: {', '.join(classes[:3])}")
        if functions:
            desc_parts.append(f"functions: {', '.join(functions[:3])}")
            
        if desc_parts:
            return f"Module containing {', '.join(desc_parts)}."
        else:
            return "Utility script or configuration module."
            
    except Exception:
        return "Python module."

def process_file(project_root, file_path):
    rel_path = os.path.relpath(file_path, project_root).replace('\\', '/')
    expected_header_1 = f"# {rel_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Skipping {rel_path} - Encoding issue.")
        return
        
    shebang = ""
    start_idx = 0
    
    # Preserve shebang if exists
    if lines and lines[0].startswith('#!'):
        shebang = lines[0]
        start_idx = 1
        
    # Check if a header already exists
    if len(lines) > start_idx and lines[start_idx].startswith('#') and lines[start_idx].strip().endswith('.py'):
        # It has a header, let's consume it so we can overwrite it
        start_idx += 1
        if len(lines) > start_idx and lines[start_idx].startswith('#'):
            start_idx += 1
            
        # Consume any blank lines immediately following the old header
        while start_idx < len(lines) and lines[start_idx].strip() == '':
            start_idx += 1

    description = generate_description(file_path)
    new_header = f"{expected_header_1}\n# {description}\n\n"
    
    # Check if we are doing a redundant write (exact match)
    # Re-read to check exact match easily
    if len(lines) >= start_idx:
        current_top = "".join(lines[:start_idx])
        if shebang + new_header.strip() in current_top and expected_header_1 in current_top:
            print(f"Skipping {rel_path} - Up to date.")
            return

    print(f"Updating {rel_path} ...")
    
    # Construct final content
    new_content = shebang + new_header + "".join(lines[start_idx:])
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    print("Starting automated header injection...")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    py_files = glob.glob(os.path.join(project_root, '**', '*.py'), recursive=True)
    count = 0
    
    for py_file in py_files:
        # Ignore virtual envs and standard hidden folders
        if any(ignore in py_file for ignore in ['.venv', 'venv', '__pycache__', '.git', '.tox']):
            continue
            
        process_file(project_root, py_file)
        count += 1
        
    print(f"\nSuccessfully processed {count} Python files.")

if __name__ == "__main__":
    main()
