from disnake import Embed, ModalInteraction

from quickUI.quickUI import QView, UserHybridSelect, user_hybrid_select

# UserHybridSelect does not require a QView so disnake.ui.View could also be used here.


class UserHybridSelectView(QView):
    @user_hybrid_select(
        placeholder="Select users",
    )
    async def user_hybrid_select(
        self, select: UserHybridSelect, interaction: ModalInteraction
    ):
        await interaction.response.defer()

        # Retrieve the mention of the members from the `values`
        member_mentions = "\n".join([f"{value.mention}" for value in select.values])

        await interaction.edit_original_message(
            embed=Embed(description=member_mentions),
            view=self,
        )
