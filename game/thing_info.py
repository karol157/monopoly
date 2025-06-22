from textual.widget import Widget
from textual.widgets import Static, Button
from textual.containers import Horizontal

from game.player.player import Player

class ThingInfo(Widget):
    def __init__(self, thing_name: str, player1:Player = Player("Player 1", 1), player2:Player = Player("Player 2", 2)):
        super().__init__()
        self.thing_name = thing_name
        self.players = [player1, player2]

    def compose(self):
        yield Static(self._text_render())
        yield Button("Buy", id="buy-button")
        yield Button("Pass", id="pass-button")

    def _text_render(self) -> str:
        return f"         {self.thing_name}       \n\n" \
               f"Price: {self.get_price()}\n" \
               f"Rent: {self.get_rent()}\n" \
               f"Owner: {self.get_owner()}\n\n\n" 
               

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-button":
            self.remove()
        
    def get_price(self) -> str:
        return "100"  
    
    def get_rent(self) -> str:
        return "10"
    
    def get_owner(self) -> str:
        return "test"
        for player in self.players:
            if self.thing_name in player.things:
                return player._name
        return "No owner"