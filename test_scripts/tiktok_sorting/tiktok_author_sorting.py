import os
import shutil
from pathlib import Path


def extract_author(filename: str) -> str | None:
    for year in ('2022', '2023', '2024', '2025'):
        if f'_{year}' in filename:
            return filename.split(f'_{year}')[0]
    return None


def organize_videos(folder: str | Path) -> None:
    folder_path = Path(folder)
    for entry in os.listdir(folder_path):
        entry_str = os.fsdecode(entry)
        entry_path = folder_path / entry_str
        if entry_path.is_file() and (author := extract_author(entry_str)):
            author_folder = folder_path / author
            author_folder.mkdir(exist_ok=True)
            shutil.move(str(entry_path), str(author_folder / entry_str))


if __name__ == '__main__':
    organize_videos(Path(r"C:\Users\Игорь\00_phone_backup\Дозагрузка\Movies\TikTok"))
