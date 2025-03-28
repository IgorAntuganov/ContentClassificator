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


def process_single_videos(root_folder: Path) -> None:
    single_folder = root_folder / 'SingleVideo'
    single_folder.mkdir(exist_ok=True)

    for author_folder in root_folder.iterdir():
        if author_folder.is_dir() and author_folder.name != 'SingleVideo':
            files = list(author_folder.glob('*'))
            video_files = [f for f in files if f.is_file()]

            if len(video_files) == 1:
                target = single_folder / video_files[0].name
                if target.exists():
                    name, suffix = target.stem, target.suffix
                    counter = 1
                    while (new_target := single_folder / f'{name}_{counter}{suffix}').exists():
                        counter += 1
                    target = new_target
                shutil.move(str(video_files[0]), str(target))
                try:
                    author_folder.rmdir()
                except OSError:
                    pass


if __name__ == '__main__':
    target_folder = Path(r'C:\Users\Игорь\00_phone_backup\Дозагрузка\Movies\TikTok')
    organize_videos(target_folder)
    process_single_videos(target_folder)
