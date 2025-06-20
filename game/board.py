from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Grid
import os

class Board(App):
    CSS_PATH = os.path.join(".." ,"src", "game.tcss")
    def compose(self) -> ComposeResult:
        names = [
            "test", "test", "test", "test", "test", "test",
            "test", "", "", "", "", "test",
            "test", "", "", "", "", "test",
            "test", "", "", "", "", "test",
            "test", "test", "test", "test", "test", "test",
        ]
        widgets = []
        for name in names:
            if name:
                widgets.append(Button(name, classes="tile"))
            else:
                widgets.append(Static("", classes="blank"))
        yield Grid(*widgets, classes="board")