from game.player.model import Model
from textual.widgets import Static

class Player(Static):
    def __init__(self, name: str, player_id: int):
        super().__init__(id=f"player-{player_id}", classes="player")
        self._name = name
        self.player_id = player_id
        self.things = []
        self.position = 0
        self.money = 1500
        self.lose_turn = 0
        self.first_after_lost_turn = False
        self.model = Model(name, self, str(self.money), self.things)
    
    def reset(self):
        self.things = []
        self.position = 0
        self.money = 1500
    
    def on_mount(self) -> None:
        self.model.on_mount()