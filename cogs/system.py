import math

import disnake
from disnake.ext import commands

import utility
from buttons.system import Dropdown, SystemView
from config.messages import Messages
from features.git import Git
from permissions import permission_check


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.git = Git()

        self.unloadable_cogs = ["system"]

    @commands.group(pass_context=True)
    async def git(self, ctx: commands.Context):
        pass

    @git.command(brief=Messages.git_pull_brief)
    @commands.check(permission_check.is_bot_admin)
    async def pull(self, ctx: commands.Context):
        message: disnake.Message = await ctx.send("Pulling")

        pull_result = await self.git.pull()
        pull_parts = utility.cut_string(pull_result, 1900)

        await message.edit(content=f"```{pull_parts[0]}```")

        for part in pull_parts[1:]:
            await ctx.send(f"```{part}```")

    @commands.check(permission_check.is_bot_admin)
    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send("shutting down")
        await self.bot.close()
        exit(0)

    async def create_selects(self):
        """Slices dictionary of all cogs to chunks for select."""
        cog_files = list(utility.get_all_cogs().keys())
        cog_names = list(utility.get_all_cogs().values())
        all_selects = []

        # 25 is max number of options for one select
        chunks = math.ceil(len(cog_files)/25)
        cog_files = list(utility.split(cog_files, chunks))
        cog_names = list(utility.split(cog_names, chunks))
        for i in range(0, chunks):
            all_selects.append([cog_files[i], cog_names[i]])

        return all_selects

    @commands.check(permission_check.is_bot_admin)
    @commands.slash_command(name="cogs", description=Messages.cogs_brief)
    async def cogs(self, inter: disnake.ApplicationCommandInteraction):
        """
        Creates embed with button and select(s) to load/unload/reload cogs.

        Max number of cogs can be 100 (4x25).
        """

        selects = await self.create_selects()
        view = SystemView(self.bot, len(selects), selects)
        embed = Dropdown.create_embed(self, inter.author.colour)
        await inter.send(embed=embed, view=view)

        # pass message object to classes
        message = await inter.original_message()
        view.message = message
        for i, cogs in enumerate(selects):
            view.selects[i].msg = message

    @cogs.error
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error.__cause__, commands.errors.ExtensionNotLoaded):
            await ctx.send(Messages.not_loaded.format(error.__cause__.name))
            return True


def setup(bot):
    bot.add_cog(System(bot))
