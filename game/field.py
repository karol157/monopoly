from textual.widgets import Button

class Field(Button):
    def __init__(self, name: str):
        self._name = name
        self._id = self.create_id()
        super().__init__(name, id=self._id, classes="tile")
    
    def on_mount(self) -> None:
        pass
    def create_id(self) -> str:
        name = self._name.replace("#", "").replace(" - ", "-").replace(" ", "-")
        return name