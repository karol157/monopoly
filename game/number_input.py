from textual.app import ComposeResult
from textual.widgets import Input, Button
from textual.widget import Widget
from textual.containers import Horizontal
from textual.screen import Screen

class NumberInput(Screen):
    def __init__(self, board, currnet_player, **kwargs):
        super().__init__(**kwargs)
        self.board = board
        self.current_player = currnet_player
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

    def compose(self) -> ComposeResult:
        with Horizontal(id="number-input-vertical"):
            yield Input(placeholder="Enter how many spaces you want to move (1-16)", name="number_input")
            yield Button("Submit", id="submit_button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_button":
            input_widget = self.query_one(Input)
            try:
                number = int(input_widget.value)
                if number <= 16 and number >= 1:
                    field_prev = self.board.query_one(f"#{self.create_id(self.fields[self.current_player.position])}")
                    self.current_player.position = (self.current_player.position + number) % 16
                    field_next = self.board.query_one(f"#{self.create_id(self.fields[self.current_player.position])}")
                    field_prev.styles.border = ("solid", "white")
                    orther_player = self.board.player2 if self.current_player.player_id == 1 else self.board.player1
                    if orther_player.position == self.current_player.position:
                        orther_player.position = (orther_player.position + number) % 16
                        field_next.styles.border = ("double", "magenta")
                    elif self.current_player.player_id == 1:
                        field_next.styles.border = ("dashed", "blue")
                    elif self.current_player.player_id == 2:
                        field_next.styles.border = ("dashed", "green")
                    self.board.query_one("#thing-info").update_info(self.current_player, self.current_player.position)
                    self.app.pop_screen()
                else:
                    raise ValueError("Number must be between 1 and 16")
            except ValueError:
                self.notify("Enter correct number", title="wrong number", severity="error")
    
    def create_id(self, field) -> str:
        name = field.replace("#", "").replace(" - ", "-").replace(" ", "-")
        return name
    
            
            
