from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def select_file(title: str, initial_dir: Path) -> Path:
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    selected = filedialog.askopenfilename(
        title=title,
        initialdir=str(initial_dir)
    )

    root.destroy()

    if not selected:
        raise RuntimeError(f"No file selected for: {title}")

    print(f"{title}: {selected}")

    return Path(selected)