# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import platform
import traceback
import tracemalloc

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext.commands import InteractionBot, errors
from dotenv import load_dotenv


class Bot(InteractionBot):
    def __init__(self, logger, logFormatter):
        self.logger = logger
        self.logFormatter = logFormatter
        intents = disnake.Intents.all()
        try:
            super().__init__(
                intents=intents, test_guilds=[int(os.getenv("TEST_GUILD_ID"))]
            )
        except TypeError as ex:
            logging.error("Parameter `TEST_GUILD_ID` from `.env` should to be an int.")
            raise ex

        extension = "tests.test"

        try:
            self.load_extension(f"{extension}")
            logging.info(f"Extension `{extension}` loaded succesfully")
        except errors.ExtensionError as ex:
            logging.error(
                f"{type(ex).__name__} during load: {ex} \n{self.tracebackEx(ex)}"
            )

    def tracebackEx(self, ex: Exception):
        if type(ex) == str:
            return "No valid traceback."
        ex_traceback = ex.__traceback__
        if ex_traceback is None:
            ex_traceback = ex.__traceback__
        tb_lines = [
            line.rstrip("\n")
            for line in traceback.format_exception(ex.__class__, ex, ex_traceback)
        ]
        return "".join(tb_lines)

    async def on_ready(self) -> None:
        """
        The code in this even is executed when the bot is ready
        """
        logging.info("-" * 50)
        logging.info(f"| Logged in as {self.user.name}")
        logging.info(f"| disnake API version: {disnake.__version__}")
        logging.info(f"| Python version: {platform.python_version()}")
        logging.info(
            f"| Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        logging.info(f"| Owner : {self.owner}")
        logging.info(f"| Bot Ready !")
        logging.info("-" * 50)
        await self.change_presence(
            activity=disnake.Activity(name="Testing disnakeQuickView")
        )

    async def send_error_log(
        self, interaction: ApplicationCommandInteraction, error: Exception
    ):
        logging.error(
            f"{error} raised on command /{interaction.application_command.name} from {interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'} by {interaction.author.name}.\n{self.tracebackEx(error)}"
        )

    async def on_slash_command(
        self, interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        logging.info(
            f"Slash command '{interaction.application_command.name}:{interaction.id}' from '{interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'}' by '{interaction.author.name}' started..."
        )

    async def on_user_command(
        self, interaction: disnake.UserCommandInteraction
    ) -> None:
        logging.info(
            f"User command '{interaction.application_command.name}:{interaction.id}' from '{interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'}' by '{interaction.author.name}' started..."
        )

    async def on_message_command(
        self, interaction: disnake.MessageCommandInteraction
    ) -> None:
        logging.info(
            f"Message command '{interaction.application_command.name}:{interaction.id}' from '{interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'}' by '{interaction.author.name}' started..."
        )

    async def on_slash_command_completion(
        self, interaction: disnake.ApplicationCommandInteraction
    ) -> None:
        logging.info(
            f"Slash command '{interaction.application_command.name}:{interaction.id}' from '{interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'}' by '{interaction.author.name}' at '{interaction.created_at}' ended normally"
        )

    async def on_user_command_completion(
        self, interaction: disnake.UserCommandInteraction
    ) -> None:
        logging.info(
            f"User command '{interaction.application_command.name}:{interaction.id}' from '{interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'}' by '{interaction.author.name}' at '{interaction.created_at}' ended normally"
        )

    async def on_message_command_completion(
        self, interaction: disnake.MessageCommandInteraction
    ) -> None:
        logging.info(
            f"Message command '{interaction.application_command.name}:{interaction.id}' from '{interaction.guild.name+'#'+interaction.channel.name if interaction.guild else 'DM'}' by '{interaction.author.name}' at '{interaction.created_at}' ended normally"
        )
