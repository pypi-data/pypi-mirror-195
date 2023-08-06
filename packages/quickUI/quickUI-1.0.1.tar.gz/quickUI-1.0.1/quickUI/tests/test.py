# -*- coding: utf-8 -*-
import disnake
from disnake.ext import commands

from examples.code_locked_view import CodelockedView
from examples.cycle_button import CycleButtonView
from examples.modal_button import ModalButtonView
from examples.modal_select import ModalSelectView
from examples.user_hybrid_select import UserHybridSelectView
from quickUI import *

from .bot import Bot


class Test(commands.Cog):
    def __init__(self, bot):
        """Initialize the cog"""
        self.bot: Bot = bot

    @commands.slash_command(
        name="test",
    )
    async def test(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @test.sub_command()
    async def cycle_button(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        test = CycleButtonView()

        await interaction.edit_original_response(
            embed=disnake.Embed(title="Test Toggle Button"), view=test
        )

    @test.sub_command()
    async def modal_button(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer(ephemeral=True)

        test = ModalButtonView()

        await interaction.edit_original_response(
            embed=disnake.Embed(title="Test Modal Button"), view=test
        )

    @test.sub_command()
    async def user_hybrid_select_button(
        self, interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        test = UserHybridSelectView()

        await interaction.edit_original_response(
            embed=disnake.Embed(title="Test User Hybrid Select"), view=test
        )

    @test.sub_command()
    async def modal_select_button(
        self, interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        test = ModalSelectView()

        await interaction.edit_original_response(
            embed=disnake.Embed(title="Test Modal Select"), view=test
        )

    @test.sub_command()
    async def code_locked_view(
        self, interaction: disnake.ApplicationCommandInteraction
    ):
        await interaction.response.defer(ephemeral=True)

        test = CodelockedView(four_digit_code="1234")

        await interaction.edit_original_response(
            embed=disnake.Embed(title="Test code locked View"), view=test
        )


def setup(bot: commands.InteractionBot):
    bot.add_cog(Test(bot))
