from disnake import ModalInteraction
from disnake.ui import Components, Modal, ModalUIComponent
from disnake.utils import MISSING

from ...interface import QItemModalInterface, QModalInterface


class QModal(Modal, QModalInterface):
    """Represents a modal to be send as a response to any item that that inherit from :class:`.QItemModalInterface`.

    This will be created by the :class:`.QItemModalInterface` and is not meant to be instanciated by the user.

    Parameters
    ----------
    title: :class:`str`
        The title of the modal.
    modal_item: :class:`.QItemModalInterface`
        The item from where this modal will be send. This can be let ``MISSING`` but need to be set before the first interaction.
    components: |components_type|
        The components to display in the modal. Up to 5 action rows.
    custom_id: :class:`str`
        The custom ID of the modal.
    timeout: :class:`float`
        The time to wait until the modal is removed from cache, if no interaction is made.
        Modals without timeouts are not supported, since there's no event for when a modal is closed.
        Defaults to 600 seconds.
    """

    def __init__(
        self,
        *,
        title: str,
        modal_item: QItemModalInterface = MISSING,
        components: Components[ModalUIComponent],
        custom_id: str = MISSING,
        timeout: float = 600,
    ) -> None:
        super().__init__(
            title=title, components=components, custom_id=custom_id, timeout=timeout
        )
        if modal_item is not MISSING:
            self.modal_item = modal_item

    @property
    def modal_item(self) -> QItemModalInterface:
        """This is the item that inherit from :class:`.QItemModalInterface` and from which this modal has been sent."""
        if not hasattr(self, "_modal_item"):
            raise AttributeError(f"'modal_item' has not been set.")
        return self._modal_item

    @modal_item.setter
    def modal_item(self, value: QItemModalInterface):
        if not issubclass(value.__class__, QItemModalInterface):
            raise TypeError(
                f"Property `modal_item` should be a subclass of `QItemModalInterface`. Provided one is of type `{value.__class__.__name__}`."
            )
        self._modal_item = value

    async def callback(self, interaction: ModalInteraction, /) -> None:
        """|coro|

        This redirect the callback from the modal to the :py:meth:`~.QItemModalInterface.modal_callback()` of the item.

        Parameters
        ----------
        interaction : :class:`~disnake.ModalInteraction`
            The interaction from the modal.
        """
        await self.modal_item.modal_callback(self, interaction)
