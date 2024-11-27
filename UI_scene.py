import UI_abstracts


class Scene:
    def __init__(self, elements: list[UI_abstracts.UIElement]):
        self.focused_element: UI_abstracts.UIElement | None = None
        self.elements = elements

    def add_element(self, element):
        self.elements.append(element)

    def handle_events(self):
        pass
