import json
import os


class JsonListStorage:
    def __init__(self, save_path: str):
        self.save_path = save_path
        self._list: list[str] = []
        self._ensure_json_exists()
        self._load_data()

    def _ensure_json_exists(self) -> None:
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        if not os.path.exists(self.save_path):
            self.save_data()

    def _load_data(self) -> None:
        with open(self.save_path, 'r', encoding='utf-8') as f:
            self._list = json.load(f)

    def save_data(self) -> None:
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(self._list, f, indent=2, ensure_ascii=False)

    # list-like methods
    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def append(self, folder: str, auto_save: bool = True):
        self._list.append(folder)
        if auto_save:
            self.save_data()

    def remove(self, folder: str, auto_save: bool = True):
        self._list.remove(folder)
        if auto_save:
            self.save_data()

    @property
    def list_copy(self) -> list[str]:
        return self._list.copy()
