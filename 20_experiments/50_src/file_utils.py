import os


def load_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def save_result(file_path, content):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        # print(" " * 7 + f"Saved result to: {file_path}\n")
    except Exception as e:
        print(" " * 7 + f"Error saving file {file_path}: {e}\n")


def slugify(text):
    return text.lower().replace(" ", "_").replace("-", "_")
