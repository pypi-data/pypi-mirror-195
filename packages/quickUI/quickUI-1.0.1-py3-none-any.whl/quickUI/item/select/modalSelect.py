from __future__ import annotations

import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_origin,
    overload,
)

from disnake import MessageInteraction, ModalInteraction
from disnake.ui import StringSelect
from disnake.ui.item import DecoratedItem, Object
from disnake.utils import MISSING

from ...interface import QItemModalInterface
from ..modal import QModal, ModalSelectOption

if TYPE_CHECKING:
    from disnake.ui.item import ItemCallbackType
    from disnake.ui.view import View
    from typing_extensions import ParamSpec

else:
    ParamSpec = TypeVar

S_co = TypeVar("S_co", bound="ModalSelect", covariant=True)
V_co = TypeVar("V_co", bound="Optional[View]", covariant=True)
P = ParamSpec("P")


class ModalSelect(StringSelect[V_co], QItemModalInterface):
    """Represents a StringSelect that send modals when options are selected.

    This should only be used in :class:`~quickUI.quickUI.view.view.QView` and its subclasses.

    .. note::
        The :py:attr:`~disnake.ui.StringSelect.min_values` and :py:attr:`~disnake.ui.StringSelect.max_values` are not available and set to ``1`` because only one modal can be sent as a response to a selection.

    Parameters
    ----------
    modal_select_options: List[:class:`.ModalSelectOption`]
        A list of options that can be selected in this menu.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
    disabled: :class:`bool`
        Whether the button is disabled.
    placeholder: Optional[:class:`str`]
        The placeholder text that is shown if nothing is selected, if any.
    disabled: :class:`bool`
        Whether the select is disabled.
    row: Optional[:class:`int`]
        The relative row this select menu belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """

    @overload
    def __init__(
        self: StringSelect[None],
        *,
        modal_select_options: List[ModalSelectOption],
        custom_id: str = ...,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self: StringSelect[V_co],
        *,
        modal_select_options: List[ModalSelectOption],
        custom_id: str = ...,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        modal_select_options: List[ModalSelectOption],
        custom_id: str = MISSING,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        self.modal_options = modal_select_options
        super().__init__(
            custom_id=custom_id,
            options=self.modal_options,
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            disabled=disabled,
            row=row,
        )

    @property
    def modal_options(self) -> List[ModalSelectOption]:
        """The list of :class:`.ModalSelectOption`."""
        return self._modals_options

    @modal_options.setter
    def modal_options(self, values: List[ModalSelectOption]) -> None:
        if not isinstance(values, list):
            raise TypeError(
                f"Property `modal_options` of `ModalSelect` should be of type List[`ModalSelectOption`] but provided one is type {values.__class__.__name__}"
            )
        if not all(isinstance(value, ModalSelectOption) for value in values):
            raise TypeError(
                f"All element of 'modal_options' should be of type 'ModalSelectOption'."
            )
        self._modals_options = values
        for modal_option in values:
            modal_option.qModal.modal_item = self

    def qModal_option_by_id(self, custom_id: str) -> ModalSelectOption:
        """Find a :class:`.ModalSelectOption` based on its custom_id.

        Parameters
        ----------
        custom_id: :class:`str`
            The custom it of the component.

        Returns
        -------
        :class:`.ModalSelectOption`
            The option that correspond to the custom_id.

        Raises
        ------
        :class:`ValueError`
            Raised if not component is found.
        """
        for qModal_option in self.modal_options:
            if qModal_option.custom_id == custom_id:
                return qModal_option
        raise ValueError(f"Can not find 'qModal_option' with {custom_id=}")

    def qModal_option_by_value(self, value: str) -> ModalSelectOption:
        """Find a :class:`.ModalSelectOption` based on its custom_id.

        Parameters
        ----------
        value: :class:`str`
            The value of the component.

        Returns
        -------
        :class:`.ModalSelectOption`
            The option that correspond to the value.

        Raises
        ------
        :class:`ValueError`
            Raised if not component is found.
        """
        for qModal_option in self.modal_options:
            if qModal_option.value == value:
                return qModal_option
        raise ValueError(f"Can not find 'qModal_option' with {value=}")

    def qModal_option_by_message_interaction(
        self, interaction: MessageInteraction
    ) -> ModalSelectOption:
        """Find the :class:`.ModalSelectOption` that triggered the interaction.

        Parameters
        ----------
        interaction: :class:`~disnake.MessageInteraction`
            The interaction that trigger the select.

        Returns
        -------
        :class:`.ModalSelectOption`
            The option that triggered the interaction.

        Raises
        ------
        :class:`ValueError`
            Raised if not component is found.
        """
        return self.qModal_option_by_value(interaction.values[0])

    def qModal_option_by_modal(self, qModal: QModal) -> ModalSelectOption:
        """Find the :class:`.ModalSelectOption` from its :class:`.QModal`.

        Parameters
        ----------
        qModal: :class:`.QModal`
            The :class:`.QModal` asociated with the :class:`.ModalSelectOption`.

        Returns
        -------
        :class:`.ModalSelectOption`
            The option that triggered the MessageInteraction.

        Raises
        ------
        :class:`ValueError`
            Raised if not component is found.
        """
        return self.qModal_option_by_id(qModal.custom_id)

    @property
    def text_values(self) -> Dict[ModalSelectOption, Dict[str, str]]:
        """A dict of the text_values from the :class:`.QModal`, associated with their :class:`.ModalSelectOption`"""
        if not hasattr(self, "_text_values"):
            self._text_values = {}
        return self._text_values

    async def qCallback(self, interaction: MessageInteraction) -> None:
        """|coro|

        This is called by the :class:`.QView` went a selection is made.

        This reponse to the interaction by sending the :class:`.QModal` associated with the option selected.

        Parameters
        ----------
        interaction: :class:`~disnake.MessageInteraction`
            The interaction that triggered the button.
        """
        await interaction.response.send_modal(
            self.qModal_option_by_message_interaction(interaction).qModal
        )

    async def modal_callback(
        self, qModal: QModal, interaction: ModalInteraction
    ) -> None:
        """|coro|

        This is called by the modal when it is filled.

        This update the :py:attr:`.text_values` then passes the interaction to the user by calling :py:meth:`.callback()`.

        Parameters
        ----------
        qModal: :class:`.QModal`
            The modal that is filled.
        interaction: :class:`~disnake.ModalInteraction`
            The interaction that trigger the end of the modal
        """
        self.text_values[self.qModal_option_by_modal(qModal)] = interaction.text_values
        await self.callback(interaction)


@overload
def modal_select(
    *,
    qModal_options: List[ModalSelectOption],
    custom_id: str = ...,
    placeholder: Optional[str] = None,
    disabled: bool = False,
    row: Optional[int] = None,
) -> Callable[[ItemCallbackType[ModalSelect[V_co]]], DecoratedItem[ModalSelect[V_co]]]:
    ...


@overload
def modal_select(
    cls: Type[Object[S_co, P]], *_: P.args, **kwargs: P.kwargs
) -> Callable[[ItemCallbackType[S_co]], DecoratedItem[S_co]]:
    ...


def modal_select(
    cls: Type[Object[V_co, P]] = ModalSelect[Any], **kwargs: Any
) -> Callable[[ItemCallbackType[S_co]], DecoratedItem[S_co]]:
    """A decorator that attaches a modal select to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`QView`, the :class:`.ModalSelect` that was
    interacted with, and the :class:`~disnake.MessageInteraction`.

    Parameters
    ----------
    cls: Type[:class:`.ModalSelect`]
        The StringSelect subclass to create an instance of. If provided, the following parameters
        described below do no apply. Instead, this decorator will accept the same keywords
        as the passed cls does.

    qModal_options: List[Union[:class:`.ModalSelectOption`, :class:`.QModal`]]
        A list of options that can be selected in this menu. Use explicit :class:`.ModalSelectOption`
        for fine-grained control over the options. Alternatively, a list of :class:`.QModal` will
        result in options with the labels set to the modal's titles.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
        If this button is for a URL, it does not have a custom ID.
    disabled: :class:`bool`
        Whether the button is disabled.
    placeholder: Optional[:class:`str`]
        The placeholder text that is shown if nothing is selected, if any.
    disabled: :class:`bool`
        Whether the select is disabled.
    row: Optional[:class:`int`]
        The relative row this select menu belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """
    if (origin := get_origin(cls)) is not None:
        cls = origin

    if not isinstance(cls, type) or not issubclass(cls, ModalSelect):
        raise TypeError(f"cls argument must be a subclass of ModalSelect, got {cls!r}")

    def decorator(func: ItemCallbackType[S_co]) -> DecoratedItem[V_co]:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("modal_select function must be a coroutine function")

        func.__discord_ui_model_type__ = cls
        func.__discord_ui_model_kwargs__ = kwargs
        return func  # type: ignore

    return decorator
