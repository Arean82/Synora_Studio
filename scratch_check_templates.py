import os
import glob
from jinja2 import Environment, FileSystemLoader

def main():
    templates_dir = os.path.abspath("synora_saas/templates")
    env = Environment(loader=FileSystemLoader(templates_dir), extensions=['jinja2.ext.i18n'])
    env.install_null_translations(newstyle=True)
    
    files = glob.glob(os.path.join(templates_dir, "**/*.html"), recursive=True)
    print(f"Checking {len(files)} templates...")
    
    errors = []
    for f in files:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                env.compile(content)
        except Exception as e:
            errors.append((f, e))
            
    if errors:
        for f, e in errors:
            print(f"ERROR in {f}: {e}")
    else:
        print("All templates compiled successfully!")

if __name__ == "__main__":
    main()
