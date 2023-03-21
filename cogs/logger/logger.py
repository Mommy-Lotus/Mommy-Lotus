from disnake.ext import commands


class Logger(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_command(self, ctx):
        guild = self.bot.get_guild(ctx.guild_id)
        self.logger.log(21, f"Guild: {guild} || Channel: {ctx.channel} || "
                            f"Message: {ctx.message.id} || Author: {ctx.author} || "
                            f"Command: {ctx.command.name} || Passed: {ctx.args}")

    @commands.Cog.listener()
    async def on_slash_command(self, inter):
        guild = self.bot.get_guild(inter.guild_id)
        self.logger.log(22, f"Guild: {guild} || Channel: {inter.channel} || "
                            f"Message: {inter.id} || Author: {inter.author} || "
                            f"Command: {inter.data.name} || Passed: {inter.filled_options}")
