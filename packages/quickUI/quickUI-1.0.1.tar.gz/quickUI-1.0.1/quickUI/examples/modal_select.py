from disnake import Embed, ModalInteraction
from disnake.ui import TextInput

from quickUI.quickUI import ModalSelect, QModalSelectOption, QView, modal_select

# TestModalSelect require a QView.


class ModalSelectView(QView):
    @modal_select(
        placeholder="Select a modal",
        qModal_options=[
            QModalSelectOption(
                title="Test Modal 1",
                components=TextInput(label="test 1.1", custom_id="test_11"),
            ),
            QModalSelectOption(
                title="Test Modal 2",
                components=[
                    TextInput(label="test 2.1", custom_id="test_21"),
                    TextInput(label="test 2.2", custom_id="test_22"),
                ],
            ),
        ],
    )
    async def modal_select(
        self, modalSelect: ModalSelect, interaction: ModalInteraction
    ):
        # This is the interaction from the modal. In this case, we only want the edit the original message so we used the 'with_message=False' to not visually response to this one.
        await interaction.response.defer(with_message=False)

        # text_values for each option are given in the 'text_values' dict.
        responses = ""
        for options, text_values in modalSelect.text_values.items():
            responses += f"__**{options.label}**__\n"
            for custom_id, value in text_values.items():
                responses += f"> __{custom_id}__: {value}\n"

        # The Message interaction is accessible by the 'ModalSelect.original_interaction' property.
        original_interaction = modalSelect.original_interaction

        # This interaction has already been answered to to send the modal, so we have to used the 'edit_original_response'.
        await original_interaction.edit_original_response(
            embed=Embed(description=responses),
            view=self,
        )
