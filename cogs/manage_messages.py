import random

import disnake
from disnake.ext import commands

from config.messages import Messages
from permissions import permission_check


class ManageMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._rand_int = 1

    @commands.Cog.listener("on_message")
    async def reply(self, message):
        """sends messages to users depending on the content"""
        if message.guild is None:
            return
        if message.author.bot:
            return

        if "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif "PR" == message.content:
            await message.channel.send(Messages.pr_link)
        elif self.bot.user.mentioned_in(message):
            if random.randint(1, self._rand_int) == 1:
                await message.channel.send(random.choice(Messages.Lotus_love))
            else:
                await message.channel.send(random.choice(Messages.Lotus))

    @commands.slash_command(name="lotus")
    async def _love(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @commands.check(permission_check.is_bot_admin)
    @_love.sub_command(name="set_love", description=Messages.Lotus_set_love_brief)
    async def set_love(self, inter: disnake.ApplicationCommandInteraction, number: int):
        self._rand_int = number
        await inter.send(Messages.Lotus_set_love.format(100/number))

    @commands.check(permission_check.is_bot_admin)
    @_love.sub_command(name="print_love", description=Messages.Lotus_print_love_brief)
    async def print_love(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(Messages.Lotus_print_love.format(100/self._rand_int))


def setup(bot):
    bot.add_cog(ManageMessages(bot))
