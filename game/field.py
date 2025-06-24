from textual.widgets import Button

class Field(Button):
    def __init__(self, name: str, price:int = 0, rent:int = 0, is_buyable: bool = True):
        self._name = name
        self._id = self.create_id()
        super().__init__(name, id=self._id, classes="tile")
        if price > 0:
            self.price = price
        if rent > 0:
            self.rent = rent
        
        self.owner = None
        self.is_buyable = is_buyable
    
    def on_mount(self) -> None:
        pass
    def create_id(self) -> str:
        name = self._name.replace("#", "").replace(" - ", "-").replace(" ", "-")
        return name