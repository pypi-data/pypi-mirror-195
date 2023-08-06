from typing import Union

from disnake import ButtonStyle, Emoji, PartialEmoji


class ButtonState:
    """Represents a state of a button.

    Parameters
    ----------
    label: :class:`str`
        The label to display on the button, if any.
    emoji: Union[:class:`str`, :class:`disnake.Emoji`, :class:`~disnake.PartialEmoji`]
        The emoji to display on the button, if any.
    style: :class:`~disnake.ButtonStyle`
        The style of the button, ``ButtonStyle.primary`` by default.
    """

    def __init__(
        self,
        label: str = None,
        emoji: Union[str, Emoji, PartialEmoji] = None,
        style: ButtonStyle = ButtonStyle.primary,
    ):
        self.label = label
        self.style = style
        self.emoji = emoji
