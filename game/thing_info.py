from textual.widget import Widget
from textual.widgets import Static, Button

from game.player.player import Player
import game.chance_and_risk as car
from game.number_input import NumberInput

import random


class ThingInfo(Widget):
    """
    Displays detailed info about a board field and allows user interaction (buy/pass).

    Handles special tiles like Chance, Risk, and Neostrada.
    """

    def __init__(
        self,
        thing_name: str,
        player1: Player = Player("Player 1", 1),
        player2: Player = Player("Player 2", 2),
        board=None,
        **kwargs,
    ):
        """
        Args:
            thing_name (str): Name of the field to initialize display.
            player1 (Player): First player.
            player2 (Player): Second player.
            board (App): Reference to the board for querying fields.
        """
        super().__init__(**kwargs)
        self.thing_name = thing_name
        self.players = [player1, player2]
        self.board = board
        self.turning_player = None
        random.shuffle(car.chances)

    def compose(self):
        """Create the info display and buttons."""
        yield Static(self._text_render(), id="info-text")
        yield Button("Buy", id="buy-button")
        yield Button("Pass", id="pass-button")

    def _text_render(self) -> str:
        """Render default field info panel text."""
        return (
            f"         {self.thing_name}       \n\n"
            f"Price: {self.get_price()}\n"
            f"Rent: {self.get_rent()}\n"
            f"Owner: {self.get_owner()}\n\n\n"
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle Buy button logic."""
        if event.button.id == "buy-button":
            price = self.get_price()
            if isinstance(price, int) and self.turning_player.money >= price:
                self.turning_player.money -= price
                self.turning_player.things.append(self.thing_name)

                field = self.board.query_one(f"#{self._field_id(self.thing_name)}")
                field.owner = self.turning_player.player_id
                field.is_buyable = False
                field.styles.color = (
                    "green" if self.turning_player.player_id == 2 else "blue"
                )

                self._refresh()
                self.board.check_win()
            else:
                self.query_one("#info-text", Static).update(
                    "Not enough money to buy this thing."
                )

    def get_price(self):
        if self.thing_name == "Start":
            return "Adding 200$"
        field = self.board.query_one(f"#{self._field_id(self.thing_name)}")
        return getattr(field, "price", "Not for sale")

    def get_rent(self):
        if self.thing_name == "Start":
            return "None"
        field = self.board.query_one(f"#{self._field_id(self.thing_name)}")
        return getattr(field, "rent", "No rent")

    def get_owner(self):
        if self.thing_name == "Start":
            return "No owner"
        field = self.board.query_one(f"#{self._field_id(self.thing_name)}")
        return self.players[field.owner - 1]._name if field.owner else "No owner"

    def _field_id(self, field_name: str) -> str:
        """Normalize field name to valid ID."""
        return field_name.replace("#", "").replace(" - ", "-").replace(" ", "-")

    def _refresh(self):
        """Refresh the info panel and player UI."""
        self.query_one("#info-text", Static).update(self._text_render())
        self.turning_player.model.update(
            self.turning_player.money, self.turning_player.things
        )

    def update_info(self, turning_player: Player, previous_position: int) -> None:
        """
        Update info panel and handle logic for special fields.

        Args:
            turning_player (Player): Player whose turn it is.
            previous_position (int): Position before movement (used for "passed Start").
        """
        self.turning_player = turning_player
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
        self._refresh()
        field = self.board.query_one(f"#{self._field_id(self.thing_name)}")

        buy_button = self.query_one("#buy-button", Button)
        pass_button = self.query_one("#pass-button", Button)

        if field.is_buyable:
            buy_button.disabled = False
            pass_button.disabled = False
        else:
            buy_button.disabled = True
            pass_button.disabled = True

            if self.thing_name in ["Chance", "Risk"]:
                self._handle_chance_or_risk(turning_player, fields)

            if field.owner and field.owner != turning_player.player_id:
                self._handle_rent_payment(turning_player, field)

            if self.thing_name == "Neostrada":
                self.app.push_screen(NumberInput(self.board, turning_player))

        # Start bonus
        if turning_player.position < previous_position:
            turning_player.money += 200
            text = self.query_one("#info-text", Static)
            text.update(
                f"Passed the Start field, adding 200$ to {turning_player._name}\n\n\n{str(text.renderable)}"
            )
            turning_player.model.update(turning_player.money, turning_player.things)

        self.board.check_win()

    def _handle_rent_payment(self, player: Player, field) -> None:
        """Transfer rent if landing on opponent's property."""
        base_rent = getattr(field, "rent", 0)
        rent = base_rent

        # Double rent if player owns similar property
        for thing in player.things:
            if thing[:-1] == self.thing_name[:-1]:
                rent *= 2

        player.money -= rent
        self.players[field.owner - 1].money += rent

        self.query_one("#info-text", Static).update(
            f"Paid {rent}$ rent to {self.players[field.owner - 1]._name}"
        )

        for p in self.players:
            p.model.update(p.money, p.things)

    def _handle_chance_or_risk(self, player: Player, fields: list[str]) -> None:
        """Apply effects from a Chance or Risk card."""
        card = car.chances.pop() if self.thing_name == "Chance" else car.risks.pop()
        car.chances.insert(0, card)

        info_lines = [card[0]]
        actions = [a.replace("_", "-") for a in card[1].split("-")]

        # Parse actions into pairs
        i, action_pairs = 0, []
        while i < len(actions):
            if actions[i] in ["mn", "mv", "lt", "rl", "rm"]:
                action_pairs.append(
                    (actions[i], actions[i + 1] if i + 1 < len(actions) else None)
                )
                i += 2
            else:
                i += 1

        for action, value in action_pairs:
            if action == "mn":
                try:
                    player.money += int(value)
                    info_lines.append(f"Money change: {value}$")
                except:
                    pass
            elif action == "mv":
                if value and value.isdigit():
                    self._move_player(player, int(value), fields)
                    info_lines.append(f"Moved by {value} fields")
                elif value == "any":
                    self.app.push_screen(NumberInput(self.board, player))
            elif action == "lt":
                player.lose_turn = getattr(player, "lose_turn", 0) + int(value)
                player.first_after_lost_turn = True
                info_lines.append(f"Lose {value} turn(s)")
            elif action == "rl" and value == "ag":
                info_lines.append("Dice rolled again")
                dice = self.board.query_one("#dice")
                dice.roll()
            elif action == "rm" and value == "any":
                if player.things:
                    removed = random.choice(player.things)
                    player.things.remove(removed)

                    field = self.board.query_one(f"#{self._field_id(removed)}")
                    field.is_buyable = True
                    field.owner = None
                    field.styles.color = "white"
                    field.styles.border = ("solid", "white")

                    player.model.update(player.money, player.things)
                    info_lines.append(f"Removed {removed}")
                else:
                    info_lines.append("No things to remove")

        existing_text = self.query_one("#info-text", Static).renderable
        self.query_one("#info-text", Static).update(
            "\n".join(info_lines) + f"\n{str(existing_text)}"
        )
        player.model.update(player.money, player.things)

    def _move_player(self, player: Player, offset: int, fields: list[str]) -> None:
        """Move player by given offset and update borders."""
        prev_field = self.board.query_one(f"#{self._field_id(fields[player.position])}")
        prev_field.styles.border = ("solid", "white")

        player.position = (player.position + offset) % len(fields)

        next_field = self.board.query_one(f"#{self._field_id(fields[player.position])}")
        if self.players[0].position == self.players[1].position:
            next_field.styles.border = ("double", "magenta")
        else:
            next_field.styles.border = (
                "dashed",
                "green" if player.player_id == 2 else "blue",
            )
