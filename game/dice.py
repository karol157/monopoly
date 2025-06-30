from textual.widgets import Static, Button
from textual.widget import Widget
from game.player.player import Player
import random


class Dice(Widget):
    """
    A widget representing a dice used to control player turns.

    Attributes:
        players (list[Player]): List of two player objects.
        turn (int): Indicates whose turn it is (1 or 2).
        value (int): The value from the last dice roll.
        board (Board): Reference to the game board instance.
        fields (list[str]): Ordered list of field names corresponding to board positions.
    """

    def __init__(
        self,
        player1: Player = Player("Player 1", 1),
        player2: Player = Player("Player 2", 2),
        board=None,
        **kwargs,
    ):
        """
        Initialize the Dice widget.

        Args:
            player1 (Player): First player object.
            player2 (Player): Second player object.
            board (App): Reference to the game board app.
        """
        super().__init__(**kwargs)
        self.players = [player1, player2]
        self.turn = None
        self.value = 0
        self.board = board
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
        self._set_starting_player()

    def compose(self):
        """Compose the dice interface layout."""
        yield Static(self._get_dice_text(), id="dice-text")
        yield Button("Roll the dice", id="roll-button")

    def _set_starting_player(self) -> None:
        """Randomly choose which player starts the game."""
        self.turn = random.choice([1, 2])

    def roll(self) -> None:
        """Perform a dice roll and update player position, board state, and UI."""
        current_player = self.players[self.turn - 1]
        other_player = self.players[1 if self.turn == 1 else 0]
        prev_position = current_player.position

        # Skip turn if flagged
        if getattr(current_player, "lose_turn", 0) > 0:
            current_player.lose_turn -= 1
            self._switch_turn()
            return

        self.value = random.randint(1, 6)
        current_player.position = (current_player.position + self.value) % len(
            self.fields
        )

        self._update_dice_text()
        self._update_field_styles(prev_position, current_player, other_player)
        self._update_thing_info(current_player, prev_position)

        self._switch_turn()

    def _update_dice_text(self) -> None:
        """Update the text shown in the dice panel."""
        dice_text = self.query_one("#dice-text", Static)
        dice_text.update(self._get_dice_text())

    def _update_field_styles(
        self, prev_position: int, current: Player, other: Player
    ) -> None:
        """
        Update field styles to visually reflect player positions.

        Args:
            prev_position (int): The position the player moved from.
            current (Player): The current player after rolling.
            other (Player): The opponent player.
        """
        prev_id = self._field_id(self.fields[prev_position])
        current_id = self._field_id(self.fields[current.position])

        prev_field = self.board.query_one(f"#{prev_id}", Button)
        curr_field = self.board.query_one(f"#{current_id}", Button)

        # Update previous field style
        if other.position == prev_position:
            prev_field.styles.border = ("dashed", "green" if self.turn == 2 else "blue")
        else:
            prev_field.styles.border = ("solid", "white")

        # Update new field style
        if self.players[0].position == self.players[1].position:
            curr_field.styles.border = ("double", "magenta")
        else:
            curr_field.styles.border = ("dashed", "blue" if self.turn == 1 else "green")

    def _update_thing_info(self, player: Player, prev_position: int) -> None:
        """
        Update the ThingInfo widget with the current player's info.

        Args:
            player (Player): The player whose info should be shown.
            prev_position (int): The previous position before the move.
        """
        thing_info = self.board.query_one("#thing-info")
        thing_info.update_info(player, prev_position)

    def _switch_turn(self) -> None:
        """Switch to the other player's turn."""
        self.turn = 2 if self.turn == 1 else 1

    def _get_dice_text(self) -> str:
        """
        Get formatted dice text content.

        Returns:
            str: Text content showing current player, field, and dice value.
        """
        player = self.players[self.turn - 1]
        return (
            f"      {player._name}      \n"
            f"\n\n"
            f"Current field: {self.fields[player.position]}\n"
            f"\n"
            f"Dice value: {self.value}\n"
            f"\n"
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle dice roll when button is pressed.

        Args:
            event (Button.Pressed): Event object from button press.
        """
        if event.button.id == "roll-button":
            self.roll()

    def _field_id(self, field_name: str) -> str:
        """
        Generate a valid widget ID from a field name.

        Args:
            field_name (str): Field name as shown on the board.

        Returns:
            str: Normalized ID string.
        """
        return field_name.replace("#", "").replace(" - ", "-").replace(" ", "-")
