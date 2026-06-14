# scripts/update_docs.py
# Utility script or configuration module.

import os
import re

root = r"c:\Users\user\OneDrive\Desktop\python\Synora_Studio"
docs_to_check = []
for dirpath, dirnames, filenames in os.walk(root):
    if "obsolete files" in dirpath:
        continue
    for f in filenames:
        if f.endswith(".md"):
            docs_to_check.append(os.path.join(dirpath, f))

replacements = [
    (re.compile(r'python desktop[\\/]desktop\.py --cli'), r'python headless/headless.py --cli'),
    (re.compile(r'python desktop[\\/]desktop\.py --list-models'), r'python headless/headless.py --list-models'),
    (re.compile(r'python desktop[\\/]desktop\.py --update-models'), r'python headless/headless.py --update-models'),
    (re.compile(r'python desktop[\\/]desktop\.py --migrate'), r'python synora_synora_server/synora_server.py --migrate'),
    (re.compile(r'python desktop[\\/]desktop\.py --api-manager'), r'python synora_synora_server/synora_server.py --api-manager'),
    (re.compile(r'python desktop\.py --cli'), r'python headless/headless.py --cli'),
    (re.compile(r'python desktop\.py --list-models'), r'python headless/headless.py --list-models'),
    (re.compile(r'python desktop\.py --update-models'), r'python headless/headless.py --update-models'),
    (re.compile(r'python desktop\.py --migrate'), r'python synora_synora_server/synora_server.py --migrate'),
    (re.compile(r'python desktop\.py --api-manager'), r'python synora_synora_server/synora_server.py --api-manager'),
]

for doc in docs_to_check:
    with open(doc, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern, repl in replacements:
        new_content = pattern.sub(repl, new_content)
        
    if new_content != content:
        with open(doc, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated docs in: {os.path.relpath(doc, root)}")
