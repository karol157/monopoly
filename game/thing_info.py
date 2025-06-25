from textual.widget import Widget
from textual.widgets import Static, Button

from game.player.player import Player

import time

class ThingInfo(Widget):
    def __init__(self, thing_name: str, player1:Player = Player("Player 1", 1), player2:Player = Player("Player 2", 2), board=None,**kwargs):
        super().__init__(**kwargs)
        self.thing_name = thing_name
        self.players = [player1, player2]
        self.board = board
        self.turning_player = None

    def compose(self):
        yield Static(self._text_render(), id="info-text")
        yield Button("Buy", id="buy-button")
        yield Button("Pass", id="pass-button")

    def _text_render(self) -> str:
        return f"         {self.thing_name}       \n\n" \
               f"Price: {self.get_price()}\n" \
               f"Rent: {self.get_rent()}\n" \
               f"Owner: {self.get_owner()}\n\n\n" 
               

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "buy-button":
            if self.turning_player.money >= int(self.get_price()):
                self.turning_player.money -= int(self.get_price())
                self.turning_player.things.append(self.thing_name)
                field = self.board.query_one(f"#{self.create_id(self.thing_name)}")
                field.owner = self.turning_player.player_id
                field.is_buyable = False
                field.styles.color = "green" if self.turning_player.player_id == 2 else "blue"
                self.query_one("#info-text", Static).update(self._text_render())
                self.turning_player.model.update(self.turning_player.money, self.turning_player.things)
            else:
                self.query_one("#info-text", Static).update("Not enough money to buy this thing.")
            
        
    def get_price(self) -> str:
        if self.thing_name == "Start":
            return "Adding 200$"
        field = self.board.query_one(f"#{self.create_id(self.thing_name)}")
        return field.price if hasattr(field, 'price') else "Not for sale"

    def get_rent(self) -> str:
        if self.thing_name == "Start":
            return "None"
        field = self.board.query_one(f"#{self.create_id(self.thing_name)}")
        return field.rent if hasattr(field, 'rent') else "No rent"

    
    def get_owner(self) -> str:
        if self.thing_name == "Start":
            return "No owner"
        field = self.board.query_one(f"#{self.create_id(self.thing_name)}")
        if field.owner is not None:
            return self.players[field.owner - 1]._name
        else:
            return "No owner"

    def update_info(self, turning_player: Player, previous_position: int) -> None:
        fields = [
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
        self.thing_name = fields[turning_player.position]
        self.query_one("#info-text", Static).update(self._text_render())
        field = self.board.query_one(f"#{self.create_id(self.thing_name)}")
        if field.is_buyable:
            self.query_one("#buy-button", Button).disabled = False
            self.query_one("#pass-button", Button).disabled = False
        else:
            if field.owner is not None and field.owner != turning_player.player_id:
                rent = field.rent if hasattr(field, 'rent') else "No rent"
                for thing in self.turning_player.things:
                    if thing[:-1] == self.thing_name[:-1]:
                        rent *= 2
                turning_player.money -= rent
                self.players[field.owner - 1].money += rent
                self.query_one("#info-text", Static).update(f"Paid {rent}$ rent to {self.players[field.owner - 1]._name}")
                for player in self.players:
                    player.model.update(player.money, player.things)
            self.query_one("#buy-button", Button).disabled = True
            self.query_one("#pass-button", Button).disabled = True
        
        if turning_player.position < previous_position:
            text_info = self.query_one("#info-text", Static)
            text_info.update(f"Passed the Start field, adding 200$ to {turning_player._name}\n\n\n{str(text_info.renderable)}")
            turning_player.money += 200
            turning_player.model.update(turning_player.money, turning_player.things)

        self.turning_player = turning_player
    def create_id(self, field) -> str:
        name = field.replace("#", "").replace(" - ", "-").replace(" ", "-")
        return name