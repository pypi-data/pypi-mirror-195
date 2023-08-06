import logging
import os
import tracemalloc

from dotenv import load_dotenv

from tests.bot import Bot

if __name__ == "__main__":
    tracemalloc.start()

    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    rootLogger.addHandler(consoleHandler)

    load_dotenv()

    bot = Bot(logger=rootLogger, logFormatter=logFormatter)

    bot.run(os.getenv("DISCORD_TOKEN"))
