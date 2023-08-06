from __future__ import annotations

import asyncio
from itertools import cycle
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    Type,
    TypeVar,
    get_origin,
    overload,
)

from disnake import MessageInteraction, Object
from disnake.ui import Button
from disnake.ui.item import DecoratedItem, Object

from ...interface import QItemInterface
from .state import ButtonState

if TYPE_CHECKING:
    from disnake.ui.item import ItemCallbackType
    from disnake.ui.view import View
    from typing_extensions import ParamSpec

else:
    ParamSpec = TypeVar

B = TypeVar("B", bound="CycleButton")
B_co = TypeVar("B_co", bound="CycleButton", covariant=True)
V_co = TypeVar("V_co", bound="Optional[View]", covariant=True)
P = ParamSpec("P")


class CycleButton(Button[V_co], QItemInterface):
    """Represents a button that cycle through multiple state when clicked.

    This should only be used in :class:`~quickUI.quickUI.view.view.QView` and its subclasses.

    Parameters
    ----------
    states: List[:class:`.ButtonState`]
        The list of state to cycle through.
    placeholder_state: Optional[:class:`.ButtonState`]
        The state to use as placeholder before the first interaction.
        If not provided, the first state is initially selected.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
    disabled: :class:`bool`
        Whether the button is disabled.
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
        states: List[ButtonState],
        placeholder_state: ButtonState = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        row: Optional[int] = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self: Button[V_co],
        *,
        states: List[ButtonState],
        placeholder_state: ButtonState = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        row: Optional[int] = None,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        states: List[ButtonState],
        placeholder_state: ButtonState = None,
        disabled: bool = False,
        custom_id: Optional[str] = None,
        row: Optional[int] = None,
    ) -> None:
        self.states = states
        self._states_iterator = cycle(states)
        self.placeholder_state = placeholder_state
        if self.placeholder_state:
            self.current_state = placeholder_state
            self._apply_state()
        else:
            self.set_next_state()

        super().__init__(
            label=self.current_state.label,
            style=self.current_state.style,
            emoji=self.current_state.emoji,
            disabled=disabled,
            custom_id=custom_id,
            row=row,
        )

    @property
    def states(self) -> List[ButtonState]:
        """The list of :class:`.ButtonState` to cycle through."""
        return self._states

    @states.setter
    def states(self, states: List[ButtonState]) -> None:
        if not isinstance(states, list):
            raise TypeError(
                f"`states` arg should be a `list`. Provided one is type {states.__class__.__name__}"
            )
        if not all(isinstance(state, ButtonState) for state in states):
            raise TypeError(f"All elements of `states` should be a `QToggleState`.")
        self._states = states

    @property
    def current_state(self) -> ButtonState:
        """The :class:`.ButtonState` that is currently selected and displayed."""
        return self._current_state

    @current_state.setter
    def current_state(self, state: ButtonState) -> None:
        if not isinstance(state, ButtonState):
            raise TypeError(
                f"`state` arg should be a `ButtonState`. Provided one is type {type(state)}"
            )
        self._current_state = state

    @property
    def placeholder_state(self) -> ButtonState:
        """The :class:`.ButtonState` used as placeholder."""
        return self._placeholder

    @placeholder_state.setter
    def placeholder_state(self, value: ButtonState):
        if value == None:
            self._placeholder = None
        elif not isinstance(value, ButtonState):
            raise TypeError(
                f"Property 'placeholder' should be a 'ButtonState'. Provided one is of type '{value.__class__.__name__}'"
            )
        else:
            self._placeholder = value

    def add_state(self, state: ButtonState, index: int = None) -> None:
        """Add a :class:`.ButtonState` to the cycling list.

        This does not change the current state.

        Parameters
        ----------
        state : :class:`.ButtonState`
            The state to add.
        index : int, optional
            The position where to insert the state, by default ``None`` mean at the end.

        Raises
        ------
        IndexError
            Raise if the provided index is higher than the size of the states list.
        """
        if index is None:
            self.states.append(state)
        else:
            if index >= len(self.states):
                raise IndexError("Argument 'index' is higher than the size of states.")
            self.states.insert(index, state)
            self._states_iterator = cycle(self.states)
            while True:
                if next(self._states_iterator) == self.current_state:
                    return

    def set_state(self, state: ButtonState) -> None:
        """Set the state of the button to a given :class:`.ButtonState`.

        The provided state should be present in the :py:attr:`.states` the button has.

        You can add state using :py:meth:`.add_state()`.

        Parameters
        ----------
        state : :class:`.ButtonState`
            The state to set.
        """
        if state not in self.states:
            raise ValueError("State provided is not in the existing list.")
        while True:
            if next(self._states_iterator) == state:
                break
        self.current_state = state
        self._apply_state()

    def set_next_state(self) -> None:
        """Set the next state of the button."""
        self.current_state = next(self._states_iterator)
        self._apply_state()

    def _apply_state(self) -> None:
        """Apply the current button state."""
        self.label = self.current_state.label
        self.style = self.current_state.style
        self.emoji = self.current_state.emoji

    async def qCallback(self, interaction: MessageInteraction) -> None:
        """|coro|

        This is called by the :class:`~quickUI.quickUI.view.view.QView` went the item is triggered.

        This set the current state to the next state of the list then passes the interaction to the user by calling :py:meth:`.callback()`.

        Parameters
        ----------
        interaction : :class:`~disnake.MessageInteraction`
            The interaction that triggered the item.
        """
        self.set_next_state()
        await self.callback(interaction)


@overload
def cycle_button(
    *,
    states: List[ButtonState],
    placeholder_state: ButtonState = None,
    disabled: bool = False,
    custom_id: Optional[str] = None,
    row: Optional[int] = None,
) -> Callable[[ItemCallbackType[CycleButton[V_co]]], DecoratedItem[CycleButton[V_co]]]:
    ...


@overload
def cycle_button(
    cls: Type[Object[B_co, P]], *_: P.args, **kwargs: P.kwargs
) -> Callable[[ItemCallbackType[B_co]], DecoratedItem[B_co]]:
    ...


def cycle_button(
    cls: Type[Object[B_co, P]] = CycleButton[Any], **kwargs: Any
) -> Callable[[ItemCallbackType[B_co]], DecoratedItem[B_co]]:
    """A decorator that attaches a cycle button to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`~quickUI.quickUI.view.view.QView`, the :class:`.CycleButton` that was
    interacted with, and the :class:`~disnake.MessageInteraction`.

    Parameters
    ----------
    cls: Type[:class:`.CycleButton`]
        The button subclass to create an instance of. If provided, the following parameters
        described below do no apply. Instead, this decorator will accept the same keywords
        as the passed cls does.

    states: List[:clacc:`.ButtonState`]
        The list of state to cycle through.
    placeholder: Optional[:class:`.ButtonState`]
        The state to use as placeholder before the first interaction.
        If not provided, the first state is initially selected.
    custom_id: Optional[:class:`str`]
        The ID of the button that gets received during an interaction.
    disabled: :class:`bool`
        Whether the button is disabled.
    row: Optional[:class:`int`]
        The relative row this button belongs to. A Discord component can only have 5
        rows. By default, items are arranged automatically into those 5 rows. If you'd
        like to control the relative positioning of the row then passing an index is advised.
        For example, row=1 will show up before row=2. Defaults to ``None``, which is automatic
        ordering. The row number must be between 0 and 4 (i.e. zero indexed).
    """

    if (origin := get_origin(cls)) is not None:
        cls = origin

    if not isinstance(cls, type) or not issubclass(cls, CycleButton):
        raise TypeError(f"cls argument must be a subclass of CycleButton, got {cls!r}")

    def decorator(func: ItemCallbackType[B_co]) -> DecoratedItem[B_co]:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("cycle_button function must be a coroutine function")

        func.__discord_ui_model_type__ = cls
        func.__discord_ui_model_kwargs__ = kwargs
        return func  # type: ignore

    return decorator
