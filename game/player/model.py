class Model:
    """
    ViewModel for representing a player's current state in the UI.

    Attributes:
        _name (str): Player's name (used in header).
        _id (str): Identifier used for styling or querying.
        money (str): Current balance as string.
        things (list[str]): List of owned property names.
        main_model (Static): The associated Textual widget to update.
    """

    def __init__(
        self,
        name: str,
        main_model,
        money: str = "1500",
        things: list[str] = None,
    ):
        """
        Initialize the player model with display values.

        Args:
            name (str): Player's name.
            main_model (Static): The Textual widget representing this model in the UI.
            money (str): Initial money value.
            things (list[str], optional): Initial list of owned items.
        """
        super().__init__()
        self._name = name
        self._id = name
        self.money = money
        self.things = things if things is not None else []
        self.main_model = main_model

        # Apply initial styles
        self.main_model.styles.border = ("heavy", "white")

    def render(self) -> str:
        """
        Render the model as a string block for display in UI.

        Returns:
            str: Rendered player info block.
        """
        owned_items = ", ".join(self.things)
        return (
            f"     {self._name}     \nMoney: {self.money}  \nThings: {owned_items}  \n"
        )

    def on_mount(self) -> None:
        """
        Called when the associated Textual widget is mounted.
        Updates the visual with current model state.
        """
        self.main_model.update(self.render())

    def update(self, money: str = None, things: list[str] = None) -> None:
        """
        Update the model's money and/or things and refresh UI.

        Args:
            money (str, optional): New money amount.
            things (list[str], optional): New list of owned items.
        """
        if money is not None:
            self.money = money
        if things is not None:
            self.things = things
        self.main_model.update(self.render())
