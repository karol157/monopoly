from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Grid, Vertical, Horizontal

from game.field import Field
from game.player.player import Player
from game.dice import Dice
from game.thing_info import ThingInfo
from game.win import WinScreen

import os


class Board(App):
    """Main application class for the Monopoly game."""

    CSS_PATH = [
        os.path.join("..", "src", "game.tcss"),
        os.path.join("..", "src", "dice.tcss"),
        os.path.join("..", "src", "thing_info.tcss"),
        os.path.join("..", "src", "number_input.tcss"),
        os.path.join("..", "src", "win.tcss"),
    ]

    def __init__(self):
        """Initialize the Monopoly board application."""
        super().__init__()
        self.title = "Monopoly game"

        # Board setup with field objects and placeholders
        self.board = [
            Field("Network card #1", 120, 10),
            Field("RAM memory #1", 140, 12),
            Field("Graphics card #1", 160, 14),
            Field("Chance", is_buyable=False),
            Field("RAM memory #2", 180, 16),
            Field("Hard drive #2", 200, 18),
            Field("Komputronik - computer service #1", 100, 8),
            "",
            "",
            "",
            "",
            Field("Processor #1", 220, 20),
            Field("Hard drive #1", 60, 4),
            "",
            "",
            "",
            "",
            Field("Network card #2", 240, 22),
            Field("Start", is_buyable=False),
            Field("Graphics card #2", 300, 28),
            Field("Risk", is_buyable=False),
            Field("Processor #2", 280, 16),
            Field("Komputronik - computer service #2", 260, 24),
            Field("Neostrada", is_buyable=False),
        ]

        # Players
        self.player1 = Player("Player 1", 1)
        self.player2 = Player("Player 2", 2)

    def compose(self) -> ComposeResult:
        """
        Compose the layout of the app.

        Returns:
            ComposeResult: Composed widgets for the UI layout.
        """
        widgets = [
            field if field else Static("", classes="blank") for field in self.board
        ]

        with Vertical():
            yield Static("Monopoly Game", classes="title")
            yield self.player1
            yield self.player2
            with Horizontal():
                yield ThingInfo(
                    "Start", self.player1, self.player2, self, id="thing-info"
                )
                yield Grid(*widgets, classes="board")
                yield Dice(self.player1, self.player2, self, id="dice")

    def check_win(self) -> None:
        """
        Check the win condition for the players.

        A player wins if:
        - The other player has no money left, or
        - The player collects all required computer parts.
        """
        required_parts = [
            "Network card",
            "RAM memory",
            "Graphics card",
            "Hard drive",
            "Processor",
        ]

        # Win by money loss
        if self.player1.money <= 0:
            self.app.push_screen(WinScreen(self.player2))
            return
        elif self.player2.money <= 0:
            self.app.push_screen(WinScreen(self.player1))
            return

        # Win by collecting full computer set
        for player in [self.player1, self.player2]:
            missing_parts = required_parts.copy()
            for thing in player.things:
                part_type = thing.rsplit(" ", 1)[0]  # Remove number suffix
                if part_type in missing_parts:
                    missing_parts.remove(part_type)
            if not missing_parts:
                self.app.push_screen(WinScreen(player))
                return
