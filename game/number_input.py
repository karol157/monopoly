from textual.app import ComposeResult
from textual.widgets import Input, Button
from textual.containers import Horizontal
from textual.screen import Screen


class NumberInput(Screen):
    """
    A screen allowing the current player to manually enter how many spaces to move.

    Attributes:
        board (App): Reference to the main game board.
        current_player (Player): The player making the move.
        fields (list[str]): Ordered list of field names on the board.
    """

    def __init__(self, board, current_player, **kwargs):
        """
        Initialize the number input screen.

        Args:
            board (App): The main game board.
            current_player (Player): The player whose turn it is.
        """
        super().__init__(**kwargs)
        self.board = board
        self.current_player = current_player
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
        """
        Compose the layout with an input field and a submit button.

        Returns:
            ComposeResult: Layout content.
        """
        with Horizontal(id="number-input-vertical"):
            yield Input(
                placeholder="Enter how many spaces you want to move (1–16)",
                name="number_input",
            )
            yield Button("Submit", id="submit_button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle logic when the submit button is pressed.

        Validates input and moves the player accordingly.

        Args:
            event (Button.Pressed): The event triggered by button press.
        """
        if event.button.id != "submit_button":
            return

        input_widget = self.query_one(Input)
        try:
            number = int(input_widget.value)
            if not (1 <= number <= 16):
                raise ValueError("Number must be between 1 and 16")

            prev_position = self.current_player.position
            new_position = (prev_position + number) % len(self.fields)

            prev_field = self.board.query_one(
                f"#{self._field_id(self.fields[prev_position])}"
            )
            next_field = self.board.query_one(
                f"#{self._field_id(self.fields[new_position])}"
            )

            # Update player position
            self.current_player.position = new_position

            # Reset previous field border
            prev_field.styles.border = ("solid", "white")

            # Determine and update other player
            other_player = (
                self.board.player2
                if self.current_player.player_id == 1
                else self.board.player1
            )

            # Handle collision on same field
            if other_player.position == new_position:
                other_player.position = (other_player.position + number) % len(
                    self.fields
                )
                next_field.styles.border = ("double", "magenta")
            else:
                color = "blue" if self.current_player.player_id == 1 else "green"
                next_field.styles.border = ("dashed", color)

            # Update side panel info
            self.board.query_one("#thing-info").update_info(
                self.current_player, new_position
            )

            self.app.pop_screen()

        except ValueError:
            self.notify("Enter correct number", title="Invalid Input", severity="error")

    def _field_id(self, field_name: str) -> str:
        """
        Convert a field name to a valid widget ID.

        Args:
            field_name (str): The field name.

        Returns:
            str: Normalized ID string.
        """
        return field_name.replace("#", "").replace(" - ", "-").replace(" ", "-")
