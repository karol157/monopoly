from textual.widgets import Static, Button
from textual import events
from textual.widget import Widget
from game.player.player import Player
import random

class Dice(Widget):

    def __init__(self, player1: Player = Player("Player 1", 1), player2: Player = Player("Player 2", 2), board=None, **kwargs):
        super().__init__(**kwargs)
        self.players = [player1, player2]
        self.turn = None
        self.value = 0
        self.board = board
        self._who_starts()
        self.fields = [
            "Start",
            "Hard drive #1",
            "Komputronik - computer service #1",
            "Network card #1",
            "RAM memory #1",
            "Graphics card #1",
            "Chance",
            "RAM memory #2",
            "Hard drive #2",
            "Processor #1",
            "Network card #2",
            "Neostrada",
            "Komputronik - computer service #2",
            "Processor #2",
            "Risk",
            "Graphics card #2",
        ]

    def compose(self):
        yield Static(self._text_content(), id="dice-text")
        yield Button("Roll the dice", id="roll-button")

    def _who_starts(self):
        self.turn = random.choice([1, 2])

    def roll(self):
        prev_position = self.players[self.turn - 1].position

        self.value = random.randint(1, 6)
    
        current = self.players[self.turn - 1]
        if hasattr(current, "lose_turn") and current.lose_turn > 0:
            current.lose_turn -= 1
            self.turn = 2 if self.turn == 1 else 1
            return
        if self.value + current.position >= 16:
            current.position = (current.position + self.value) % 16
        else:
            current.position += self.value
        
        dice_text = self.query_one("#dice-text", Static)
        dice_text.update(self._text_content())

        other_player = self.players[1 if self.turn - 1 == 0 else 0]
        other_on_prev = other_player.position == prev_position

        prev_field = self.board.query_one(f"#{self.create_id(self.fields[prev_position])}", Button)
        if not other_on_prev:
            prev_field.styles.border = ("solid", "white")
        else:
            if self.turn == 1:
                prev_field.styles.border = ("dashed", "green")
            else:
                prev_field.styles.border = ("dashed", "blue")

        target_field = self.board.query_one(f"#{self.create_id(self.fields[self.players[self.turn - 1].position])}", Button)
        if self.players[0].position == self.players[1].position:
            target_field.styles.border = ("double", "magenta")
        elif self.turn == 1:
            target_field.styles.border = ("dashed", "blue")
        else:
            target_field.styles.border = ("dashed", "green")

        self.board.query_one("#thing-info").update_info(self.players[self.turn - 1], prev_position)

        self.turn = 2 if self.turn == 1 else 1

    def _text_content(self) -> str:
        return f"      {self.players[self.turn - 1]._name}      \n" \
               f"\n\n" \
               f"Current field: {self.fields[self.players[self.turn - 1].position]}\n" \
               f"\n" \
               f"Dice value: {self.value}\n" \
               f"\n" 
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "roll-button":
            self.roll()
            

    def create_id(self, field) -> str:
        name = field.replace("#", "").replace(" - ", "-").replace(" ", "-")
        return name