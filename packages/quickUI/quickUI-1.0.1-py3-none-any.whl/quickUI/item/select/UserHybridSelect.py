from __future__ import annotations

import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_origin,
    overload,
)

from disnake import Member, Role, User
from disnake.ui import MentionableSelect
from disnake.ui.item import DecoratedItem, Object
from disnake.ui.select.base import V_co
from disnake.utils import MISSING

if TYPE_CHECKING:
    from disnake.ui.item import ItemCallbackType
    from disnake.ui.view import View
    from typing_extensions import ParamSpec

else:
    ParamSpec = TypeVar

S_co = TypeVar("S_co", bound="UserHybridSelect", covariant=True)
V_co = TypeVar("V_co", bound="Optional[View]", covariant=True)
P = ParamSpec("P")


class UserHybridSelect(MentionableSelect[V_co]):
    """Represents select item that allow to select Union[:class:`~disnake.User`, :class:`~disnake.Member`]'s from Union[:class:`~disnake.User`, :class:`~disnake.Member`, :class:`~disnake.Role`]'s.

    This does not required a :class:`~quickUI.quickUI.view.view.QView` and is completely compatible with classical :class:`disnake.ui.View`.

    This make sure that all items available in the :py:attr:`.values` property are Union[:class:`~disnake.User`, :class:`~disnake.Member`] by extracting the :class:`~disnake.Member` from :class:`~disnake.Role` without duplicate.

    .. note::
        The :py:attr:`~disnake.ui.StringSelect.min_values` and :py:attr:`~disnake.ui.StringSelect.max_values` are not available here because the size of :py:attr:`.values` is not directly related to the the number of Union[:class:`~disnake.User`, :class:`~disnake.Member`, :class:`~disnake.Role`] selected by the users.
        Therefor, the maximal limit are used (:py:attr:`~disnake.ui.StringSelect.min_values` = 1, :py:attr:`~disnake.ui.StringSelect.max_values` = 25).

    Parameters
    ----------
    custom_id: :class:`str`
        The ID of the select menu that gets received during an interaction.
        If not given then one is generated for you.
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
        self: MentionableSelect[None],
        *,
        custom_id: str = ...,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        ...

    @overload
    def __init__(
        self: MentionableSelect[V_co],
        *,
        custom_id: str = ...,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        ...

    def __init__(
        self,
        *,
        custom_id: str = MISSING,
        placeholder: Optional[str] = None,
        disabled: bool = False,
        row: Optional[int] = None,
    ) -> None:
        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            min_values=1,
            max_values=25,
            disabled=disabled,
            row=row,
        )

    @property
    def values(self) -> List[Union[Member, User]]:
        """Selected values, with :class:`~disnake.Member`'s extracted from :class:`~disnake.Role` and no duplicate"""
        members: List[Union[Member, User]] = []
        for value in super().values:
            if isinstance(value, User) or isinstance(value, Member):
                if value not in members:
                    members.append(value)
            elif isinstance(value, Role):
                for member in value.members:
                    if member not in members:
                        members.append(member)
        return members


@overload
def user_hybrid_select(
    *,
    custom_id: str = ...,
    placeholder: Optional[str] = None,
    disabled: bool = False,
    row: Optional[int] = None,
) -> Callable[
    [ItemCallbackType[UserHybridSelect[V_co]]], DecoratedItem[UserHybridSelect[V_co]]
]:
    ...


@overload
def user_hybrid_select(
    cls: Type[Object[S_co, P]], *_: P.args, **kwargs: P.kwargs
) -> Callable[[ItemCallbackType[S_co]], DecoratedItem[S_co]]:
    ...


def user_hybrid_select(
    cls: Type[Object[V_co, P]] = UserHybridSelect[Any], **kwargs: Any
) -> Callable[[ItemCallbackType[S_co]], DecoratedItem[S_co]]:
    """A decorator that attaches a user hybrid select to a component.

    The function being decorated should have three parameters, ``self`` representing
    the :class:`~disnake.ui.View`, the :class:`.UserHybridSelect` that was
    interacted with, and the :class:`~disnake.MessageInteraction`.

    Parameters
    ----------
    cls: Type[:class:`.UserHybridSelect`]
        The MentionableSelect subclass to create an instance of. If provided, the following parameters
        described below do no apply. Instead, this decorator will accept the same keywords
        as the passed cls does.

    custom_id: :class:`str`
        The ID of the select menu that gets received during an interaction.
        If not given then one is generated for you.
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

    if not isinstance(cls, type) or not issubclass(cls, UserHybridSelect):
        raise TypeError(
            f"cls argument must be a subclass of UserHybridSelect, got {cls!r}"
        )

    def decorator(func: ItemCallbackType[S_co]) -> DecoratedItem[V_co]:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("user_hybrid_select function must be a coroutine function")

        func.__discord_ui_model_type__ = cls
        func.__discord_ui_model_kwargs__ = kwargs
        return func  # type: ignore

    return decorator
