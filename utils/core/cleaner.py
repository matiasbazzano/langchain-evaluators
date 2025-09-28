import os
import shutil


def clean_pycache(path="."):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            if d == "__pycache__":
                full_path = os.path.join(root, d)
                try:
                    shutil.rmtree(full_path)
                except Exception as e:
                    print(f"⚠️ Could not remove {full_path}: {e}")
