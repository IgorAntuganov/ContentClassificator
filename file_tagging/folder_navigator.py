from __future__ import annotations
from pathlib import Path
from typing import Optional


class FolderNode:
    def __init__(
        self,
        name: str,
        parent: Optional[FolderNode] = None,
        path: Optional[Path] = None
    ):
        self.name = name
        self.parent = parent
        self.children: dict[str, FolderNode] = {}
        self.path = path or Path(name)

    def add_child(self, child: FolderNode) -> None:
        self.children[child.name] = child


class FileSystemNavigator:
    def __init__(self, root_path: str | Path):
        self.root = Path(root_path).expanduser().resolve()
        if not self.root.is_dir():
            raise ValueError("Not a directory")

        # Building folder tree
        self.root_node = FolderNode(name=self.root.name, path=self.root)
        self.current_node = self.root_node
        self._build_tree(self.root, self.root_node)

    def _build_tree(self, path: Path, parent_node: FolderNode) -> None:
        """Рекурсивное построение дерева папок"""
        for entry in path.iterdir():
            if entry.is_dir():
                node = FolderNode(name=entry.name, parent=parent_node, path=entry)
                parent_node.add_child(node)
                self._build_tree(entry, node)

    def list_dirs(self) -> list[str]:
        return list(self.current_node.children.keys())

    def cd(self, dir_name: str) -> None:
        if dir_name not in self.current_node.children:
            raise ValueError(f"Директория '{dir_name}' не найдена")
        self.current_node = self.current_node.children[dir_name]

    def cd_up(self) -> None:
        if self.current_node.parent is not None:
            self.current_node = self.current_node.parent

    @property
    def current_path(self) -> Path:
        return self.current_node.path

    def __repr__(self) -> str:
        return f"FileSystemNavigator(current_path='{self.current_path}')"
