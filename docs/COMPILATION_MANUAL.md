# Synora Studio Compilation Manual (For Beginners)

This manual will walk you through exactly how to take the raw Python code of Synora Studio and "compile" it into a standalone, click-to-run Linux application (like a `.deb` installer or an `.AppImage`). 

You do this when you want to give the app to someone else who doesn't have Python installed.

---

## Step 1: Prepare the Environment
Before you can compile the code, you need to have the Python environment set up with all the necessary dependencies installed.

Open your terminal, go to the `Synora_Studio` folder, and type:
```bash
# 1. Activate your virtual environment
source venv/bin/activate

# 2. Install PyInstaller (the tool that does the actual compiling)
pip install pyinstaller
```

---

## Step 2: Compile the Code
The application is now modular, meaning you can compile each component individually. Each directory contains its own `.spec` file.

To compile the Desktop GUI:
```bash
cd desktop
pyinstaller desktop.spec
```

To compile the Headless Server:
```bash
cd server
pyinstaller server.spec
```

To compile the Web Portal:
```bash
cd web
pyinstaller web.spec
```

Your screen will output a lot of text for a few minutes. PyInstaller is hunting down every single Python library your app uses and packing them together. 
When it finishes, you will see a new folder named `dist/`. Inside `dist/`, you will find your compiled executable!

---

## Step 3: Package the App for Distribution
Now that the app is compiled inside the `dist` folder, you probably want to turn it into a single installable file so you can easily send it to users. 

We have written two automated scripts to do this for you.

### Option A: Build a `.deb` Installer
If your users are on Ubuntu, Debian, or Linux Mint, they use `.deb` installers (similar to `.msi` on Windows).

Run these commands:
```bash
# Give the script permission to run
chmod +x build_deb.sh

# Execute the script
./build_deb.sh
```
When it finishes, you will see a file named `synorastudio_9.0.0.deb` in your main folder. You can double-click this file on any Ubuntu computer to install the app!

### Option B: Build an `.AppImage`
An AppImage is a single file that runs on almost *any* Linux distribution without needing to be installed at all.

Run these commands:
```bash
# Give the script permission to run
chmod +x build_appimage.sh

# Execute the script
./build_appimage.sh
```
When it finishes, it will produce a single `.AppImage` file. You can simply send this file to anyone, and they can double-click it to launch Synora Studio instantly!
