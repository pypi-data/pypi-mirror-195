from disnake import ButtonStyle, Embed, MessageInteraction

from quickUI.quickUI import ButtonState, CycleButton, QView, cycle_button


# This require a QView
class CycleButtonView(QView):
    @cycle_button(
        states=[
            ButtonState(label=f"state {i+1}") for i in range(4)
        ],  # Generate 4 state (1,2,3,4)
        placeholder_state=ButtonState(
            label="Choose state", style=ButtonStyle.secondary
        ),
    )
    async def cycle_button(
        self, cycleButton: CycleButton, interaction: MessageInteraction
    ):
        await interaction.response.defer()

        # Find the label of the state that is currently selected and that will be display on the button.
        current_state = cycleButton.current_state.label

        await interaction.edit_original_message(
            embed=Embed(
                description=f"Current state is {current_state}",
            ),
            view=self,
        )
