# synora_saas/web_scripts/update_templates.py
# Module containing functions: process_html_file, main, repl.

import os
import re

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find text nodes inside HTML elements that are not scripts/styles or empty
    # This is a basic heuristics-based approach to extract common hardcoded strings.
    # It looks for > text < patterns.
    
    def repl(match):
        text = match.group(1)
        # Skip if it's already translated or contains jinja tags or is whitespace/symbols
        if "{{" in text or "%}" in text or text.strip() == "" or text.isnumeric():
            return f">{text}<"
        
        # Skip if it looks like just punctuation
        if re.match(r'^[^\w\d]*$', text.strip()):
            return f">{text}<"
            
        stripped = text.strip()
        leading_spaces = text[:len(text) - len(text.lstrip())]
        trailing_spaces = text[len(text.rstrip()):]
        
        # Wrap the stripped text in Jinja translation tag
        new_text = f"{leading_spaces}{{{{ _('{stripped}') }}}}{trailing_spaces}"
        return f">{new_text}<"

    # We use a non-greedy match between > and <
    # We must not run this inside <script> or <style> tags.
    # First, let's temporarily hide script and style blocks
    scripts = {}
    
    def hide_script(m):
        key = f"__SCRIPT_{len(scripts)}__"
        scripts[key] = m.group(0)
        return key
        
    content = re.sub(r'<script.*?</script>', hide_script, content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style.*?</style>', hide_script, content, flags=re.DOTALL | re.IGNORECASE)
    
    # Now replace > text <
    new_content = re.sub(r'>([^<]+)<', repl, content)
    
    # Restore script/style blocks
    for key, val in scripts.items():
        new_content = new_content.replace(key, val)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

def main():
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                process_html_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
