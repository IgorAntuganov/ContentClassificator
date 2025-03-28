from pathlib import Path
from typing import List, Tuple


def convert_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} GB"


def get_folder_size(path: Path) -> int:
    total = 0
    for entry in path.rglob("*"):
        if entry.is_file():
            try:
                total += entry.stat().st_size
            except (PermissionError, FileNotFoundError):
                continue
    return total


def get_sorted_folders(root: Path) -> List[Tuple[Path, int]]:
    folders = []
    for entry in root.iterdir():
        if entry.is_dir():
            folders.append((entry, get_folder_size(entry)))
    return sorted(folders, key=lambda x: x[1], reverse=True)


def print_folder_sizes(root_folder: Path) -> None:
    for folder, size in get_sorted_folders(root_folder):
        print(f"{folder.name} — {convert_size(size)}")


if __name__ == "__main__":
    print_folder_sizes(Path(r"C:\Users\Игорь\00_phone_backup\Дозагрузка\Movies\TikTok"))
