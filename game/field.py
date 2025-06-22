from textual.widgets import Button

class Field(Button):
    def __init__(self, name: str):
        super().__init__(name, id=name, classes="tile")
        self._name = name
        self._id = name
    
    def on_mount(self) -> None:
        pass