import logging
from logging.handlers import TimedRotatingFileHandler

from cogs.logger.logger import Logger


def my_logger(default_name):
    """define log file name"""
    base_filename, ext, date = default_name.split(".")
    return f"{base_filename}.{date}.{ext}"


msg_logger = logging.getLogger("messages")
msg_logger.setLevel(logging.INFO)
msg_handler = TimedRotatingFileHandler(
    filename="logs/L.log", when="midnight",
    interval=1, encoding='utf-8', backupCount=365
    )
msg_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
msg_handler.namer = my_logger
msg_logger.addHandler(msg_handler)

logging.addLevelName(21, "TEXT_COMM")
logging.addLevelName(22, "SLASH_COMM")


disnake_logger = logging.getLogger("disnake")
disnake_logger.setLevel(logging.INFO)
disnake_handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w')
disnake_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
disnake_logger.addHandler(disnake_handler)


def setup(bot):
    bot.add_cog(Logger(bot, msg_logger))


def teardown(_):
    msg_logger.removeHandler(msg_handler)
    msg_handler.close()
