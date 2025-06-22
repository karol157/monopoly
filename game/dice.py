from textual.widgets import Static, Button
from textual import events
from textual.widget import Widget
from game.player.player import Player
import random

class Dice(Widget):

    def __init__(self, player1: Player = Player("Player 1", 1), player2: Player = Player("Player 2", 2)):
        super().__init__()
        self.players = [player1, player2]
        self.turn = None
        self.value = 0
        self._who_starts()

    def compose(self):
        # Static text section at top, Button at bottom
        yield Static(self._text_content(), id="dice-text")
        yield Button("Roll the dice", id="roll-button")

    def _who_starts(self):
        self.turn = random.choice([1, 2])

    def roll(self):
        self.value = random.randint(1, 6)
        current = self.players[self.turn - 1]
        current.position += self.value
        # toggle turn
        self.turn = 2 if self.turn == 1 else 1

    def _text_content(self) -> str:
        fields = ["test" for _ in range(16)]
        return f"      {self.players[self.turn - 1]._name}      \n" \
               f"\n\n" \
               f"Current field: {fields[self.players[self.turn - 1].position]}\n" \
               f"\n" \
               f"\n"
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "roll-button":
            self.roll()
            # update the Static text
            dice_text = self.query_one("#dice-text", Static)
            dice_text.update(self._text_content())
