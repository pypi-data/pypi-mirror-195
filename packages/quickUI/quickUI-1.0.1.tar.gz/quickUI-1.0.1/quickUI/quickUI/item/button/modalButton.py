from __future__ import annotations

import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
    get_origin,
    overload,
)

from disnake import (
    ButtonStyle,
    Emoji,
    MessageInteraction,
    ModalInteraction,
    PartialEmoji,
)
from disnake.ui import Button, Components, ModalUIComponent
from disnake.ui.item import DecoratedItem, Object

from ...interface import QItemModalInterface
from ..modal import QModal

if TYPE_CHECKING:
    from disnake.ui.item import ItemCallbackType
    from disnake.ui.view import View
    from typing_extensions import ParamSpec

else:
    ParamSpec = TypeVar

B = TypeVar("B", bound="ModalButton")
B_co = TypeVar("B_co", bound="ModalButton", covariant=True)
V_co = TypeVar("V_co", bound="Optional[View]", covariant=True)
P = ParamSpec("P")


class ModalButton(Button[V_co], QItemModalInterface):
    """Represents a button that sent a modal when clicked.

    This should only be used in :class:`~quickUI.quickUI.view.view.QView` and its subclasses.

    Parameters
    ----------
    title: :class:`str`
        The title of the modal. This is also used for the button's label if not provided.
    modal_components: |components_type|
        The components to display in the modal. Up to 5 action rows.
    modal_timeout: :class:`float`
        The time to wait until the modal is removed from cache, if no interaction is made.
        Modals without timeouts are not supported, since there's no event for when a modal is closed.
        Defaults to 600 seconds.
    style: :class:`~disnake.ButtonStyle`
        The initial style of the button. ``ButtonStyle.secondary`` by default.
    style_done: :class:`~disnake.ButtonStyle`
        The style of the button once the modal has been filled at least once. ``ButtonStyle.primary`` by default.
    label: Optional[:class:`str`]
        The label of the button. If not provided, used the title.
    disabled: :class:`bool`
        Whether the button is disabled.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
    emoji: Optional[Union[:class:`~disnake.PartialEmoji`, :class:`~disnake.Emoji`, :class:`str`]]
        The emoji of the button, if available.
    row: Optional[:class:`int`]
        The relative row this button belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """

    @overload
    def __init__(
        self: Button[None],
        *,
        title: str,
        modal_components: Components[ModalUIComponent],
        modal_timeout: float = 600,
        style: ButtonStyle = ButtonStyle.secondary,
        style_done: ButtonStyle = ButtonStyle.primary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
        row: Optional[int] = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self: Button[V_co],
        *,
        title: str,
        modal_components: Components[ModalUIComponent],
        modal_timeout: float = 600,
        style: ButtonStyle = ButtonStyle.secondary,
        style_done: ButtonStyle = ButtonStyle.primary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
        row: Optional[int] = None,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        title: str,
        modal_components: Components[ModalUIComponent],
        modal_timeout: float = 600,
        style: ButtonStyle = ButtonStyle.secondary,
        style_done: ButtonStyle = ButtonStyle.primary,
        label: Optional[str] = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
        row: Optional[int] = None,
    ) -> None:
        if label == None and emoji == None:
            label = title
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            emoji=emoji,
            row=row,
        )
        self.modal = QModal(
            modal_item=self,
            title=title,
            components=modal_components,
            timeout=modal_timeout,
        )
        self.style_done = style_done

    @property
    def text_values(self) -> Optional[Dict[str, str]]:
        """The text_values Dict[:class:`str`, :class:`str`] from the associated :class:`.QModal` last interaction, if any."""
        return self._text_values if hasattr(self, "_text_values") else None

    @text_values.setter
    def text_values(self, text_values: Dict[str, str]) -> None:
        if not isinstance(text_values, dict):
            raise TypeError(
                f"Property `text_values` of {self.__class__.__name__} should be a `dict`. Provided one is type {type(text_values)}"
            )
        if not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in text_values.items()
        ):
            raise TypeError(
                f"All elements of property `text_values` should be a pair of `str`."
            )
        self._text_values = text_values

    @property
    def modal(self) -> QModal:
        """The :class:`.QModal` to be send when the button is triggered."""
        return self._modal

    @modal.setter
    def modal(self, modal: QModal) -> None:
        if not isinstance(modal, QModal):
            raise TypeError(
                f"Property `qModal` of {self.__class__.__name__} should be a subclass of `QModalIntf` but provided one is type {type(modal)}"
            )
        self._modal = modal

    @property
    def style_done(self) -> ButtonStyle:
        """The style to apply when the modal has been filled at least once."""
        return self._style_done

    @style_done.setter
    def style_done(self, style: ButtonStyle) -> None:
        if not isinstance(style, ButtonStyle):
            raise TypeError(
                f"Property 'style_done' should be of type 'ButtonStyle'. Provided one is a {style.__class__.__name__}"
            )
        self._style_done = style

    async def qCallback(self, interaction: MessageInteraction) -> None:
        """|coro|

        This is called by the :class:`~quickUI.quickUI.view.view.QView` went the button is triggered.

        This reponse to the interaction by sending the associated :class:`.QModal`.

        Parameters
        ----------
        interaction : :class:`~disnake.MessageInteraction`
            The interaction that triggered the button.
        """
        await interaction.response.send_modal(self.modal)

    async def modal_callback(
        self, qModal: QModal, interaction: ModalInteraction
    ) -> None:
        """|coro|

        This is called by the modal when it is filled.

        This store the text_values in the :py:attr:`.text_values` property, change the style to the :py:attr:`.style_done` then passes the interaction to the user by calling :py:meth:`.callback()`.

        Parameters
        ----------
        qModal : :class:`.QModal`
            The modal that is filled.
        interaction : :class:`~disnake.ModalInteraction`
            The interaction that trigger the end of the modal
        """
        self.text_values = interaction.text_values
        self.style = self.style_done
        await self.callback(interaction)


@overload
def modal_button(
    *,
    title: str,
    modal_components: Components[ModalUIComponent],
    modal_timeout: float = 600,
    style: ButtonStyle = ButtonStyle.secondary,
    style_done: ButtonStyle = ButtonStyle.primary,
    label: Optional[str] = None,
    disabled: bool = False,
    custom_id: Optional[str] = None,
    emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
    row: Optional[int] = None,
) -> Callable[[ItemCallbackType[ModalButton[V_co]]], DecoratedItem[ModalButton[V_co]]]:
    ...


@overload
def modal_button(
    cls: Type[Object[B_co, P]], *_: P.args, **kwargs: P.kwargs
) -> Callable[[ItemCallbackType[B_co]], DecoratedItem[B_co]]:
    ...


def modal_button(
    cls: Type[Object[B_co, P]] = ModalButton[Any], **kwargs: Any
) -> Callable[[ItemCallbackType[B_co]], DecoratedItem[B_co]]:
    """A decorator that attaches a modal button to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`~quickUI.quickUI.view.view.QView`, the :class:`.ModalButton` that was
    interacted with, and the :class:`~disnake.MessageInteraction`.

    Parameters
    ----------
    cls: Type[:class:`.ModalButton`]
        The button subclass to create an instance of. If provided, the following parameters
        described below do no apply. Instead, this decorator will accept the same keywords
        as the passed cls does.

    title: :class:`str`
        The title of the modal. This is also used for the button's label if not provided.
    modal_components: |components_type|
        The components to display in the modal. Up to 5 action rows.
    modal_timeout: :class:`float`
        The time to wait until the modal is removed from cache, if no interaction is made.
        Modals without timeouts are not supported, since there's no event for when a modal is closed.
        Defaults to 600 seconds.
    style: :class:`.ButtonStyle`
        The initial style of the button. `ButtonStyle.secondary` by default.
    style_done: :class:`.ButtonStyle`
        The style of the button once the modal has been filled at least once. `ButtonStyle.primary` by default.
    label: Optional[:class:`str`]
        The label of the button. If not provided, used the title.
    disabled: :class:`bool`
        Whether the button is disabled.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
    emoji: Optional[Union[:class:`~disnake.PartialEmoji`, :class:`~disnake.Emoji`, :class:`str`]]
        The emoji of the button, if available.
    row: Optional[:class:`int`]
        The relative row this button belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """
    if (origin := get_origin(cls)) is not None:
        cls = origin

    if not isinstance(cls, type) or not issubclass(cls, ModalButton):
        raise TypeError(f"cls argument must be a subclass of ModalButton, got {cls!r}")

    def decorator(func: ItemCallbackType[B_co]) -> DecoratedItem[B_co]:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("modal_button function must be a coroutine function")

        func.__discord_ui_model_type__ = cls
        func.__discord_ui_model_kwargs__ = kwargs
        return func  # type: ignore

    return decorator
