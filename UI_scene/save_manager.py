import json
import os
from dataclasses import asdict

from constants.configs import SavableConfig
from UI_elements.abstract_element import UIElement


class SaveManager:
    def __init__(self, scene_name: str):
        self.scene_name = scene_name
        self.save_path = f"UI_scene/{scene_name}/elements.json"
        self._scene_data: dict[str, dict]  = {}
        self._registered_elements: dict[str, UIElement] = {}

        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        if not os.path.exists(self.save_path):
            self._save_scene_state()

        self._scene_data = self._load_scene_state()

    def _load_scene_state(self) -> dict[str, dict]:
        if not os.path.exists(self.save_path):
            return {}

        try:
            with open(self.save_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_scene_state(self):
        with open(self.save_path, 'w') as f:
            json.dump(self._scene_data, f, indent=2)

    def register_and_configure(self, elements_dict: dict[str, UIElement]):
        self._registered_elements = elements_dict.copy()

        for name, element in self._registered_elements.items():
            saved_data = self._scene_data.get(name)
            if saved_data:
                element.set_savable_config(SavableConfig(**saved_data))

    def commit_changes(self):
        for name, element in self._registered_elements.items():
            self._scene_data[name] = asdict(element.get_savable_config())
        self._save_scene_state()
