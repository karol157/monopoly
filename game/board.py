from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Grid, Vertical, Horizontal

from game.field import Field
from game.player.player import Player
from game.dice import Dice
from game.thing_info import ThingInfo

import os

class Board(App):
    CSS_PATH = [os.path.join(".." ,"src", "game.tcss"), os.path.join(".." ,"src", "dice.tcss"), os.path.join(".." ,"src", "thing_info.tcss")]
    def __init__(self):
        super().__init__()
        self.title = "Monopoly game"
        self.board = [
            Field("Network card #1"), Field("RAM memory #1"), Field("Graphics card #1"), Field("Chance"), Field("RAM memory #2"), Field("Hadr drive #2"),
            Field("Komputronik - computer service #1"), "", "", "", "", Field("Processor #1"),
            Field("Hard drive #1"), "", "", "", "", Field("Network card #2"),
            Field("Start"), Field("Graphics card #2"), Field("Risk"), Field("Processor #2"), Field("Komputronik - computer service #2"), Field("Neostrada"),
        ]
        self.player1 = Player("Player 1", 1)
        self.player2 = Player("Player 2", 2)
    def compose(self) -> ComposeResult:
        widgets = []
        for name in self.board:
            if name:
                widgets.append(name)
            else:
                widgets.append(Static("", classes="blank"))

        yield Static("Monopoly Game", classes="title")
        yield self.player1
        yield self.player2
        with Horizontal():
            yield ThingInfo("test1", self.player1, self.player2)
            yield Grid(*widgets, classes="board")
            yield Dice(self.player1,self.player2, self)
