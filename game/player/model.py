from textual.widgets import Static

class Model:
    def __init__(self, name: str, main_model, money: str = "1500", things: list = []):
        super().__init__()
        self._name = name
        self._id = name
        self.money = money
        self.things = things
        self.main_model = main_model

        self.main_model.styles.border = ("heavy" ,"white")

    def render(self) -> str:
        return f"     {self._name}     \n" \
               f"Money: {self.money}  \n" \
               f"Things: {str(self.things).replace("[", "").replace("]", "").replace("'", "")}  \n" \

    def on_mount(self) -> None:
        self.main_model.update(self.render())
    
    def update(self, money: str = None, things: list = None) -> None:
        if money is not None:
            self.money = money
        if things is not None:
            self.things = things
        self.main_model.update(self.render())