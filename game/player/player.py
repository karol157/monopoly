from game.player.model import Model
from textual.widgets import Static


class Player(Static):
    """
    Represents a Monopoly player with their current game state and UI model.

    Attributes:
        _name (str): Player's name.
        player_id (int): Unique ID for the player (1 or 2).
        things (list[str]): List of owned fields.
        position (int): Current position on the board.
        money (int): Current balance.
        lose_turn (int): How many turns the player should skip.
        first_after_lost_turn (bool): Whether the player is just returning from skipped turns.
        model (Model): Textual UI model reflecting the player's state.
    """

    def __init__(self, name: str, player_id: int):
        """
        Initialize a new player and their model.

        Args:
            name (str): Player's display name.
            player_id (int): ID (should be 1 or 2).
        """
        super().__init__(id=f"player-{player_id}", classes="player")
        self._name = name
        self.player_id = player_id
        self.things = []
        self.position = 0
        self.money = 1500
        self.lose_turn = 0
        self.first_after_lost_turn = False

        # Model handles UI representation
        self.model = Model(name, self, str(self.money), self.things)

    def reset(self):
        """
        Reset the player's state (position, money, owned items).
        """
        self.things = []
        self.position = 0
        self.money = 1500
        self.lose_turn = 0
        self.first_after_lost_turn = False
        self.model.update(str(self.money), self.things)

    def on_mount(self) -> None:
        """
        Hook that runs after the widget is mounted.
        Ensures the model is also mounted in the UI.
        """
        self.model.on_mount()
