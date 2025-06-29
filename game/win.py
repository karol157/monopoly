from textual import events
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Center, Horizontal

class WinScreen(Screen):
    def __init__(self,winner, **kwargs):
        super().__init__(**kwargs)
        self.width = self.size.width
        self.winner = winner

    def _on_resize(self, event: events.Resize) -> None:
        self.width = self.size.width
        self.update_padding()

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static("- WIN -", id="title"),
                Static("Congratulations", id="message"),
                Static(
                    f"Winner: {self.winner._name}\n",
                    id="information",
                ),
                Vertical(
                    Horizontal(
                        Vertical(
                            Button("Replay", id="replay", variant="success")
                        ),
                        Vertical(Static(expand=True), id="row"),
                        Vertical(
                            Button("Exit", id="exit", variant="error")
                        ),
                    ),
                    id="button-box",
                ),
                id="main-box",
            ),
            id="Container",
        )

    def _on_mount(self, event: events.Mount) -> None:
        self.update_padding()

    def update_padding(self):
        box = self.query_one("#Container")
        self.width = self.size.height
        padding = int(self.width  * 0.25)
        box.styles.padding = padding

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "replay":
            self.app.pop_screen()
        elif event.button.id == "exit":
            self.app.exit()