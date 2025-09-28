import os
import shutil
import stat

PROJECT_FOLDERS = ["agents", "evaluators", "utils", "settings"]


def handle_remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clean_pycache(base_path="."):
    for folder in PROJECT_FOLDERS:
        target = os.path.join(base_path, folder)
        if not os.path.exists(target):
            continue
        for root, dirs, files in os.walk(target):
            for d in dirs:
                if d == "__pycache__":
                    full_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(full_path, onerror=handle_remove_readonly)
                    except Exception as e:
                        print(f"⚠️ Could not remove {full_path}: {e}")


if __name__ == "__main__":
    clean_pycache()
