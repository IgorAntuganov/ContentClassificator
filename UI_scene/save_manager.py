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
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_scene_state(self):
        with open(self.save_path, 'w') as f:
            json.dump(self._scene_data, f, indent=2)

    def update_configs(self, elements_dict: dict[str, UIElement]):
        for unic_name in elements_dict:
            element = elements_dict[unic_name]
            saved_data = self._scene_data.get(unic_name, {})

            args1 = asdict(element.get_savable_config())
            args2 = saved_data
            updated_args = {**args1, **args2}
            element.set_savable_config(SavableConfig(**updated_args))

    def save_elements(self, elements_dict: dict[str, UIElement]):
        for unic_name in elements_dict:
            element = elements_dict[unic_name]
            self._scene_data[unic_name] = asdict(element.get_savable_config())
            self._save_scene_state()
