from textual.widgets import Button


class Field(Button):
    """
    Represents a tile on the game board, such as a property or special action field.

    Attributes:
        _name (str): The display name of the field.
        _id (str): Generated ID for the widget.
        price (int): Price of the field if it is buyable.
        rent (int): Rent to pay when another player lands on it.
        owner (Optional[Player]): The player who owns the field.
        is_buyable (bool): Whether this field can be bought.
    """

    def __init__(
        self,
        name: str,
        price: int = 0,
        rent: int = 0,
        is_buyable: bool = True,
    ):
        """
        Initialize the Field button widget.

        Args:
            name (str): Name of the field.
            price (int): Purchase cost of the field (default 0).
            rent (int): Rent charged when another player lands on it (default 0).
            is_buyable (bool): Indicates if the field can be bought (default True).
        """
        self._name = name
        self._id = self._generate_id()

        # Initialize base Button with styling
        super().__init__(label=name, id=self._id, classes="tile")

        # Assign only if values are greater than 0
        self.price = price if price > 0 else 0
        self.rent = rent if rent > 0 else 0

        self.owner = None
        self.is_buyable = is_buyable

    def on_mount(self) -> None:
        """
        Called when the widget is added to the app.

        Currently unused, but can be extended for animations or visual effects.
        """
        pass

    def _generate_id(self) -> str:
        """
        Generate a valid widget ID from the field name.

        Returns:
            str: Normalized ID string (safe for Textual selectors).
        """
        return self._name.replace("#", "").replace(" - ", "-").replace(" ", "-")
