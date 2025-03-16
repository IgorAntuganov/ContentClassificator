from pathlib import Path

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')


def get_image_list(folder_path: str):
    folder = Path(folder_path).resolve()
    lst = []
    for f in folder.iterdir():
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
            lst.append(str(f.absolute()))
    return lst


if __name__ == "__main__":
    print(*get_image_list(r"D:\phone backup 1\Pictures\Screenshot"))
