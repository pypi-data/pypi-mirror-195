from typing import Union

from disnake import MessageInteraction, ModalInteraction
from disnake.errors import NotFound


class QBaseInterface:
    """Represent the interface for basic QItem.

    This is used by the :class:`~quickUI.quickUI.view.view.QView` to differenciate it from the classic item.

    This is not meant to be inherited. Used the :class:`.QItemInterface` and :class:`.QItemModalInterface` subclasses instead.
    """

    async def callback(
        self, interaction: Union[MessageInteraction, ModalInteraction]
    ) -> None:
        """|coro|

        This is similarly to the classic :py:meth:`~disnake.ui.Item.callback()` but the interaction given may be either a :class:`~disnake.MessageInteraction` or a :class:`~disnake.ModalInteraction`.

        The type of the interaction is overwrited in the :class:`.QItemInterface` and :class:`.QItemModalInterface` subclasses.

        Parameters
        ----------
        interaction : Union[:class:`~disnake.MessageInteraction`, :class:`~disnake.ModalInteraction`]
            The interaction that triggered the item.
        """
        pass

    async def qCallback(self, interaction: MessageInteraction) -> None:
        """|coro|

        This is called by the :class:`~quickUI.quickUI.view.view.QView` went the item is triggered.

        This is meant to be overwrited in a subclass to allow advance behaviour.

        When overwrited in a subclass, if you don't reponse to the interaction you should pass it to the user using :py:meth:`.callback()`.

        Parameters
        ----------
        interaction : :class:`~disnake.MessageInteraction`
            The interaction that triggered the item.
        """
        pass


class QItemInterface(QBaseInterface):
    """Represent the interface for QItem that does not send a modal when trigered.

    This has a similar interface than :class:`.QBaseInterface` but overwrite the :py:meth:`~.QBaseInterface.callback()` argument's type to :class:`~disnake.MessageInteraction`
    """

    async def callback(self, interaction: MessageInteraction) -> None:
        """|coro|

        The callback associated with this UI item.

        This can be overriden by subclasses.

        This is called at the end of the :py:meth:`.qCallback()`.

        Parameters
        ----------
        interaction : :class:`~disnake.MessageInteraction`
            The interaction that triggered the item.
        """
        pass


class QItemModalInterface(QBaseInterface):
    """Represent the interface for QItem that send a modal when trigered and then callback when the modal is filled.

    This inherite from :class:`.QBaseInterface` but overwrite the :py:meth:`~.QBaseInterface.callback()` argument's type to :class:`~disnake.ModalInteraction`.

    This add the :py:meth:`.modal_callback()` to be called by the modal when it is filled.

    This also add the :py:attr:`.original_interaction` property to temporaly store the :class:`~disnake.MessageInteraction` from the button in order to be able to access it when modal is filled and the :py:meth:`.callback()` is called.
    """

    @property
    def original_interaction(self) -> MessageInteraction:
        """This is the interaction that triggered to button and to which the modal has been sent as response.

        This has already been reponsed to and further responses should be done using :py:meth:`~disnake.MessageInteraction.edit_original_response()`.
        """
        if not hasattr(self, "_original_interaction"):
            raise NotFound
        return self._original_interaction

    @original_interaction.setter
    def original_interaction(self, interaction: MessageInteraction) -> None:
        if not isinstance(interaction, MessageInteraction):
            raise TypeError
        self._original_interaction = interaction

    async def modal_callback(
        self, qModal: "QModalInterface", interaction: ModalInteraction
    ) -> None:
        """|coro|

        This is called by the modal when it is filled.

        This is meant to be overwrited in a subclass to allow advance behaviour.

        When overwrited in a subclass, if you don't reponse to the interaction you should pass it to the user using :py:meth:`.callback()`.

        Parameters
        ----------
        qModal : :class:`.QModalInterface`
            The modal that is filled.
        interaction : :class:`~disnake.ModalInteraction`
            The interaction that trigger the end of the modal
        """
        pass

    async def callback(self, interaction: ModalInteraction) -> None:
        """|coro|

        The callback associated with this UI item.

        This can be overriden by subclasses.

        This is called at the end of the :py:meth:`.modal_callback()`.

        The argument's type is :class:`~disnake.ModalInteraction` since this is triggered by the modal.

        To access the :class:`~disnake.MessageInteraction` that triggered the button, you can use the :py:attr:`.original_interaction` property.

        Parameters
        ----------
        interaction : :class:`~disnake.ModalInteraction`
            The interaction that triggered the end of the modal.
        """
        pass


class QModalInterface:
    """Represent the interface for a modal to be send as response to a MessageInteraction.

    This is only there to have a coherent typing for :class:`.QItemModalInterface`.
    """
