from typing import Optional, Union

from disnake import Emoji, PartialEmoji, SelectOption
from disnake.ui import Components, ModalUIComponent
from disnake.utils import MISSING

from .modal import QModal


class ModalSelectOption(SelectOption):
    """Represents the select option for the :class:`~quickUI.quickUI.item.select.modalSelect.ModalSelect`.

    This store the :class:`.QModal` to be send when this option is selected.

    Parameters
    ----------
    title: :class:`str`
        The title of the modal.
    components: |components_type|
        The components to display in the modal. Up to 5 action rows.
    custom_id: :class:`str`
        The custom ID of the modal.
    timeout: :class:`float`
        The time to wait until the modal is removed from cache, if no interaction is made.
        Modals without timeouts are not supported, since there's no event for when a modal is closed.
        Defaults to 600 seconds.
    label: :class:`str`
        The label of the option. This is displayed to users.
        Can only be up to 100 characters. If no provided, the modal's title is used instead.
    description: Optional[:class:`str`]
        An additional description of the option, if any.
        Can only be up to 100 characters.
    emoji: Optional[Union[:class:`str`, :class:`~disnake.Emoji`, :class:`~disnake.PartialEmoji`]]
        The emoji of the option, if available.
    default: :class:`bool`
        Whether this option is selected by default.
    """

    def __init__(
        self,
        *,
        title: str,
        components: Components[ModalUIComponent],
        custom_id: str = MISSING,
        modal_timeout: float = 600,
        label: str = None,
        description: Optional[str] = None,
        emoji: Optional[Union[str, Emoji, PartialEmoji]] = None,
        default: bool = False,
    ) -> None:
        super().__init__(
            label=label if label else title,
            description=description,
            emoji=emoji,
            default=default,
        )
        self.qModal = QModal(
            title=title,
            components=components,
            timeout=modal_timeout,
            custom_id=custom_id,
        )

    @property
    def qModal(self) -> QModal:
        """The :class:`.QModal` to be send when this option is selected."""
        return self._qModal

    @qModal.setter
    def qModal(self, value: QModal) -> None:
        if not isinstance(value, QModal):
            raise TypeError(
                f"Property 'qModal' of '{self.__class__.__name__}' should be of type 'QModal'. Provided one is of type '{value.__class__.__name__}'"
            )
        self._qModal = value

    @property
    def custom_id(self) -> str:
        """The custom_id of the associated :class:`.QModal`."""
        return self.qModal.custom_id
