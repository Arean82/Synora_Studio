# synora_saas/build.py
# Synora Studio - Web Portal Build Script

"""
Synora Studio - Web Portal Build Script
"""
import os
import subprocess
import sys

def main():
    print("Building Synora Studio SaaS Web Portal...")
    cwd = os.path.dirname(os.path.abspath(__file__))
    subprocess.check_call(["pyinstaller", "synora_saas.spec", "--noconfirm"], cwd=cwd)
    print("Web Portal build completed successfully.")

if __name__ == "__main__":
    main()
