from disnake import ButtonStyle, Embed, ModalInteraction
from disnake.ui import TextInput

from quickUI.quickUI import ModalButton, QView, modal_button


class ModalButtonView(QView):
    @modal_button(
        title="Test Modal Button",
        modal_components=[
            TextInput(label="Test 1", custom_id="test_1"),
            TextInput(label="Test 2", custom_id="test_2"),
        ],
        style=ButtonStyle.red,
        style_done=ButtonStyle.green,
    )
    async def modal_btn(self, modalButon: ModalButton, interaction: ModalInteraction):
        # This is the interaction from the modal. In this case, we only want the edit the original message so we used the 'with_message=False' to not visually response to this one.
        await interaction.response.defer(with_message=False)

        # text_values of the modal are given in the 'text_values' dict.
        responses = ""
        for custom_id, value in modalButon.text_values.items():
            responses += f"> __{custom_id}__: {value}\n"

        # The Message interaction is accessible by the 'ModalSelect.original_interaction' property.
        original_interaction = modalButon.original_interaction

        # This interaction has already been answered to to send the modal, so we have to used the 'edit_original_response'.
        await original_interaction.edit_original_response(
            embed=Embed(description=responses),
            view=self,
        )
