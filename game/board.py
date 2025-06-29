from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Grid, Vertical, Horizontal

from game.field import Field
from game.player.player import Player
from game.dice import Dice
from game.thing_info import ThingInfo
from game.number_input import NumberInput
from game.win import WinScreen

import os

class Board(App):
    CSS_PATH = [os.path.join(".." ,"src", "game.tcss"), os.path.join(".." ,"src", "dice.tcss"), os.path.join(".." ,"src", "thing_info.tcss"), os.path.join(".." ,"src", "number_input.tcss"), os.path.join(".." ,"src", "win.tcss")]
    def __init__(self):
        super().__init__()
        self.title = "Monopoly game"
        self.board = [
            Field("Network card #1", 120, 10), Field("RAM memory #1", 140, 12), Field("Graphics card #1", 160, 14), Field("Chance", is_buyable=False), Field("RAM memory #2", 180, 16), Field("Hard drive #2", 200, 18),
            Field("Komputronik - computer service #1", 100, 8), "", "", "", "", Field("Processor #1", 220, 20),
            Field("Hard drive #1", 60, 4), "", "", "", "", Field("Network card #2", 240, 22),
            Field("Start", is_buyable=False), Field("Graphics card #2", 300, 28), Field("Risk", is_buyable=False), Field("Processor #2", 280, 16), Field("Komputronik - computer service #2", 260, 24), Field("Neostrada", is_buyable=False),
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
        with Vertical():
            yield Static("Monopoly Game", classes="title")
            yield self.player1
            yield self.player2
            with Horizontal():
                yield ThingInfo("Start", self.player1, self.player2, self, id="thing-info")
                yield Grid(*widgets, classes="board")
                yield Dice(self.player1,self.player2, self, id="dice")

    def check_win(self) -> None:
        things_to_complete_computer = [
            "Network card", "RAM memory", "Graphics card",
            "Hard drive", "Processor",
        ]
        if self.player1.money <= 0:
            self.app.push_screen(WinScreen(self.player2))
        elif self.player2.money <= 0:
            self.app.push_screen(WinScreen(self.player1))
        else:
            for player in [self.player1, self.player2]:
                things_cp = things_to_complete_computer
                for thing in player.things:
                    if thing[:-2] in things_cp:
                        things_cp.remove(thing[:-2])
                if not things_cp:
                    self.app.push_screen(WinScreen(player))
                    return
