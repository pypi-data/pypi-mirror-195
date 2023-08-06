import time

from disnake import MessageInteraction
from disnake.ui.item import Item
from disnake.ui.view import View

from ..interface import QBaseInterface, QItemModalInterface


class QView(View):
    """Represent a view that support :class:`.QBaseInterface`'s subclasses.

    All view that used :class:`.QBaseInterface`'s subclasses should inherite from this.

    This is compatible with all other classical :class:`~disnake.ui.item.Item` as well as all classical :class:`~disnake.ui.View` usage.

    Parameters
    ----------
    timeout: Optional[:class:`float`]
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    """

    async def _scheduled_task(self, item: Item, interaction: MessageInteraction):
        try:
            if self.timeout:
                self.__timeout_expiry = time.monotonic() + self.timeout

            allow = await self.interaction_check(interaction)
            if not allow:
                return

            if isinstance(item, QBaseInterface):
                if isinstance(item, QItemModalInterface):
                    item.original_interaction = interaction
                await item.qCallback(interaction)
            else:
                await item.callback(interaction)
        except Exception as e:
            return await self.on_error(e, item, interaction)
