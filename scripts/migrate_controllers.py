import os
import shutil

root = r"c:\Users\user\OneDrive\Desktop\python\Synora_Studio"

# Move chat_controller
src1 = os.path.join(root, "desktop", "core", "chat_controller.py")
dst1 = os.path.join(root, "headless", "cli", "chat_controller.py")
shutil.move(src1, dst1)
print(f"Moved {src1} to {dst1}")

# Move settings_controller
src2 = os.path.join(root, "desktop", "core", "settings_controller.py")
dst2 = os.path.join(root, "server", "logic", "settings_controller.py")
shutil.move(src2, dst2)
print(f"Moved {src2} to {dst2}")
