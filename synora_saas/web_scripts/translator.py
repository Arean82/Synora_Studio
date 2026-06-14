# synora_saas/web_scripts/translator.py
# Module containing functions: translate_po_files, translate_readmes.

import os
import sys
import glob
from deep_translator import GoogleTranslator
import polib

def translate_po_files():
    locales_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'locales'))
    print(f"Scanning locales directory: {locales_dir}")
    
    if not os.path.exists(locales_dir):
        print("Locales directory not found. Please run pybabel extract and init first.")
        return

    po_files = glob.glob(os.path.join(locales_dir, '**', '*.po'), recursive=True)
    
    for po_file_path in po_files:
        # Extract language code from path (e.g. synora_saas/locales/es/LC_MESSAGES/messages.po -> es)
        parts = po_file_path.split(os.sep)
        try:
            lang_idx = parts.index('locales') + 1
            target_lang = parts[lang_idx]
        except ValueError:
            target_lang = 'en'
            
        # deep-translator uses standard 2-letter codes for most languages
        print(f"\nProcessing {po_file_path} for language: {target_lang}")
        
        try:
            po = polib.pofile(po_file_path)
            translator = GoogleTranslator(source='auto', target=target_lang[:2])
            
            changes = 0
            for entry in po:
                if not entry.msgstr and entry.msgid:
                    translated = translator.translate(entry.msgid)
                    entry.msgstr = translated
                    changes += 1
                    print(f"[{target_lang}] '{entry.msgid}' -> '{translated}'")
            
            if changes > 0:
                po.save(po_file_path)
                print(f"Saved {changes} new translations to {po_file_path}")
            else:
                print("No new translations needed.")
        except Exception as e:
            print(f"Error processing {po_file_path}: {e}")

def translate_readmes():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    saas_docs_dir = os.path.join(project_root, 'synora_saas', 'saas_docs')
    en_docs_dir = os.path.join(saas_docs_dir, 'en')
    
    if not os.path.exists(en_docs_dir):
        print(f"Docs folder not found: {en_docs_dir}")
        return
        
    readmes = glob.glob(os.path.join(en_docs_dir, '*.md'))
    
    locales_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'locales'))
    target_langs = sys.argv[1:]
    if not target_langs and os.path.exists(locales_dir):
        existing_langs = [d for d in os.listdir(locales_dir) if os.path.isdir(os.path.join(locales_dir, d))]
        target_langs = [l for l in existing_langs if l != 'en']
    
    for readme_path in readmes:
        print(f"\nTranslating Document: {readme_path}")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic chunking to avoid limits (deep-translator limit is 5000 chars)
        chunks = [content[i:i+4500] for i in range(0, len(content), 4500)]
        
        for lang in target_langs:
            lang_dir = os.path.join(saas_docs_dir, lang)
            os.makedirs(lang_dir, exist_ok=True)
            
            base_name = os.path.basename(readme_path)
            out_path = os.path.join(lang_dir, base_name)
            
            if os.path.exists(out_path):
                print(f"Skipping {out_path}, already exists.")
                continue
                
            print(f"Generating {out_path} ...")
            try:
                translator = GoogleTranslator(source='auto', target=lang)
                translated_chunks = []
                for chunk in chunks:
                    translated_chunks.append(translator.translate(chunk))
                
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write("".join(translated_chunks))
                print(f"Created {out_path}")
            except Exception as e:
                print(f"Failed to translate document to {lang}: {e}")

if __name__ == '__main__':
    translate_po_files()
    translate_readmes()
