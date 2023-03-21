"""All checks for role and user permissions"""

from typing import Union

import disnake
from disnake.ext import commands

from config.app_config import config
from config.messages import Messages


class NotAdminError(commands.CommandError):
    """An error indicating that a user doesn't have permissions to use
    a command that is available only to admins of bot.
    """
    def __init__(self) -> None:
        self.message = Messages.bot_admin_only


def is_bot_admin(ctx: Union[commands.Context, disnake.ApplicationCommandInteraction]):
    """Check if user is bot admin"""
    if ctx.author.id in config.admin_ids:
        return True
    raise NotAdminError
