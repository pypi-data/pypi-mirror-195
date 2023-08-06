from typing import Optional

from disnake import Embed, MessageInteraction

from quickUI.quickUI import *

# This make used of the QConfirmationView and the CycleButton to create a lock view that only allow to confirm when the code is correct.

# Generate 10 state (0 -> 9)
digit_states = [ButtonState(label=str(i)) for i in range(10)]


class CodelockedView(ConfirmationView):
    def __init__(self, *, four_digit_code: str, timeout: Optional[float] = 180) -> None:
        self.four_digit_code = four_digit_code
        super().__init__(timeout=timeout)

    # This only enable the confirmation button when the provided code equal the 'self.four_digit_code'
    def check(self) -> bool:
        return all(
            [
                self.digit_1.label == self.four_digit_code[0],
                self.digit_2.label == self.four_digit_code[1],
                self.digit_3.label == self.four_digit_code[2],
                self.digit_4.label == self.four_digit_code[3],
            ]
        )

    # Here the four cycle_button are the 4 digit of the locker
    @cycle_button(
        states=digit_states,
    )
    async def digit_1(self, cycleButton: CycleButton, interaction: MessageInteraction):
        await interaction.response.defer()
        self.update_confirmation_button()
        await interaction.edit_original_message(view=self)

    @cycle_button(
        states=digit_states,
    )
    async def digit_2(self, cycleButton: CycleButton, interaction: MessageInteraction):
        await interaction.response.defer()
        self.update_confirmation_button()
        await interaction.edit_original_message(view=self)

    @cycle_button(
        states=digit_states,
    )
    async def digit_3(self, cycleButton: CycleButton, interaction: MessageInteraction):
        await interaction.response.defer()
        self.update_confirmation_button()
        await interaction.edit_original_message(view=self)

    @cycle_button(
        states=digit_states,
    )
    async def digit_4(self, cycleButton: CycleButton, interaction: MessageInteraction):
        await interaction.response.defer()
        self.update_confirmation_button()
        await interaction.edit_original_message(view=self)

    # Send a congratulation message when unlocked
    async def on_confirm(self, interaction: MessageInteraction) -> None:
        await interaction.response.edit_message(
            embed=Embed(description="Congratulation, you have unlocked the view !"),
            view=None,
        )
        await interaction.delete_original_response(delay=10)

    # Send a consulation message when ragequit
    async def on_cancel(self, interaction: MessageInteraction) -> None:
        await interaction.response.edit_message(
            embed=Embed(
                description=f"Small tips for the next time: the code is **{self.four_digit_code}**"
            ),
            view=None,
        )
        await interaction.delete_original_response(delay=5)
