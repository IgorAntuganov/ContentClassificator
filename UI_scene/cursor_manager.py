import pygame


class CursorManager:
    # noinspection SpellCheckingInspection
    # # PyCharm marking these pygame elements as typo
    system_cursors = {
        'arrow': pygame.SYSTEM_CURSOR_ARROW,
        'ibeam': pygame.SYSTEM_CURSOR_IBEAM,
        'wait': pygame.SYSTEM_CURSOR_WAIT,
        'crosshair': pygame.SYSTEM_CURSOR_CROSSHAIR,
        'waitarrow': pygame.SYSTEM_CURSOR_WAITARROW,
        'sizenwse': pygame.SYSTEM_CURSOR_SIZENWSE,
        'sizenesw': pygame.SYSTEM_CURSOR_SIZENESW,
        'sizewe': pygame.SYSTEM_CURSOR_SIZEWE,
        'sizens': pygame.SYSTEM_CURSOR_SIZENS,
        'sizeall': pygame.SYSTEM_CURSOR_SIZEALL,
        'no': pygame.SYSTEM_CURSOR_NO,
        'hand': pygame.SYSTEM_CURSOR_HAND,
    }
    base_cursor_key = 'arrow'
    assert base_cursor_key in system_cursors
    current_cursor: str = base_cursor_key

    def _set_cursor_from_current(self):
        cursor = self.system_cursors[self.current_cursor]
        pygame.mouse.set_cursor(cursor)

    def set_cursor(self, cursor_key: str):
        assert cursor_key in self.system_cursors
        self.current_cursor = cursor_key
        self._set_cursor_from_current()

    def clear_cursor(self):
        self.current_cursor = self.base_cursor_key
        self._set_cursor_from_current()

    def get_current_cursor(self) -> str | None:
        return self.current_cursor
