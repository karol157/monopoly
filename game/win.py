from textual import events
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Center, Horizontal


class WinScreen(Screen):
    """
    A screen that displays the winner at the end of the game.

    Attributes:
        winner (Player): The winning player.
        width (int): Current screen width, used for padding calculations.
    """

    def __init__(self, winner, **kwargs):
        """
        Initialize the win screen with a winner.

        Args:
            winner (Player): The player who won the game.
        """
        super().__init__(**kwargs)
        self.winner = winner
        self.width = 0

    def compose(self) -> ComposeResult:
        """
        Compose the UI layout for the win screen.

        Returns:
            ComposeResult: The UI elements to be rendered.
        """
        yield Center(
            Vertical(
                Static("- WIN -", id="title"),
                Static("Congratulations", id="message"),
                Static(f"Winner: {self.winner._name}\n", id="information"),
                Vertical(
                    Horizontal(
                        Vertical(Static(expand=True), id="row"),
                        Vertical(Button("Exit", id="exit", variant="error")),
                    ),
                    id="button-box",
                ),
                id="main-box",
            ),
            id="Container",
        )

    def _on_mount(self, event: events.Mount) -> None:
        """
        Called when the screen is mounted. Initializes layout.
        """
        self.update_padding()

    def _on_resize(self, event: events.Resize) -> None:
        """
        Called when the screen is resized. Updates layout padding.

        Args:
            event (Resize): Resize event containing new dimensions.
        """
        self.width = self.size.width
        self.update_padding()

    def update_padding(self) -> None:
        """
        Adjust padding based on current screen width.
        """
        container = self.query_one("#Container")
        self.width = self.size.width
        container.styles.padding = int(self.width * 0.25)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button press events.

        Args:
            event (Button.Pressed): The button press event.
        """
        if event.button.id == "exit":
            self.app.exit()
