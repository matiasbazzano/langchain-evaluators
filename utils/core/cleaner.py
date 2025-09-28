import os
import shutil

PROJECT_FOLDERS = ["agents", "evaluators", "resources", "utils"]


def clean_pycache(base_path="."):
    for folder in PROJECT_FOLDERS:
        target = os.path.join(base_path, folder)
        if not os.path.exists(target):
            continue
        for root, dirs in os.walk(target):
            for d in dirs:
                if d == "__pycache__":
                    full_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(full_path)
                    except Exception as e:
                        print(f"⚠️ Could not remove {full_path}: {e}")
