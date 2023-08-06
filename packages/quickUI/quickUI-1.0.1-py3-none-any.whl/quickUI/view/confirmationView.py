from enum import Enum
from typing import Callable, Optional

from disnake import ButtonStyle, MessageInteraction
from disnake.ui import Button, button

from .view import QView


class ViewState(Enum):
    PENDING_OR_TIMEOUT = 0
    CONFIRMED = 1
    CANCELLED = 2


class ConfirmationView(QView):
    """Represents a subclasses of :class:`.QView` that already contains a :py:attr:`.confirm_button` and a :py:attr:`.cancel_button` button.

    Once the view has finished, the three differents ending state can be check with the property:

    - :py:attr:`.is_confirmed`
    - :py:attr:`is_cancelled`
    - :py:attr:`is_timeout`

    The :py:attr:`.confirm_button` enable/disable state can be set using the :py:attr:`.check_confirm` callable argument that will be used in the method :py:meth:`.update_confirmation_button()`.

    The :py:attr:`.check_confirm` callable argument can be set in two ways:
    - at instanciation by passing a Callable[[:class:`.ConfirmationView`], `bool`] to the ``check`` argument.
    - by subclass this and overwriting the :py:meth:`.check()` method to return a `bool`.

    Parameters
    ----------
    check: Callable[[:class:`.ConfirmationView`], :class:`bool`]
        The function used to enable/disable the :py:attr:`.confirm_button`. This take this view as only positional argument and should return ``True`` to enable the button and ``False`` to disable it.
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    """

    def __init__(
        self,
        *,
        check: Callable[["ConfirmationView"], bool] = None,
        timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(timeout=timeout)
        self._state = ViewState.PENDING_OR_TIMEOUT
        if not self._subclass_check_exist():
            self.check_confirm = check if check else (lambda: False)
        self.update_confirmation_button()

    @property
    def is_confirmed(self) -> bool:
        return self._state == ViewState.CONFIRMED

    @property
    def is_cancelled(self) -> bool:
        return self._state == ViewState.CANCELLED

    @property
    def is_timeout(self) -> bool:
        return self._state == ViewState.PENDING_OR_TIMEOUT and self.__stopped.done()

    def check(self) -> bool:
        return None

    def _subclass_check_exist(self) -> bool:
        return self.check() != None
        # return (getattr(self, 'check', None) != None and callable(getattr(self, 'check')))

    def update_confirmation_button(self) -> None:
        """Enable/disable the :py:attr:`.confirm_button` depending on the response of the :py:attr:`.check_confirm` callable."""
        if self._subclass_check_exist():
            self.confirm_button.disabled = not self.check()
        else:
            self.confirm_button.disabled = not self.check_confirm(self)

    @button(label="Confirm", emoji="✅", style=ButtonStyle.green, row=4)
    async def confirm_button(self, button: Button, interaction: MessageInteraction):
        self._state = ViewState.CONFIRMED
        self.stop()
        await self.on_confirm(interaction)

    @button(label="Cancel", emoji="❌", style=ButtonStyle.red, row=4)
    async def cancel_button(self, button: Button, interaction: MessageInteraction):
        self._state = ViewState.CONFIRMED
        self.stop()
        await self.on_cancel(interaction)

    async def on_confirm(self, interaction: MessageInteraction) -> None:
        """|coro|

        Event callback when the :py:attr:`.confirm_button` is triggered.

        This is meant to be overwrite in subclass.

        Parameters
        ----------
        interaction: :class:`~disnake.MessageInteraction`
            The interaction that triggered the button.
        """
        pass

    async def on_cancel(self, interaction: MessageInteraction) -> None:
        """|coro|

        Event callback when the :py:attr:`.cancel_button` is triggered.

        This is meant to be overwrite in subclass.

        Parameters
        ----------
        interaction : :class:`~disnake.MessageInteraction`
            The interaction that triggered the button.
        """
        pass
