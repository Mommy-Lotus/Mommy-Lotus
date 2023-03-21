import traceback

import disnake
from disnake import Embed
from disnake.ext import commands

import utility
from config.app_config import config
from config.messages import Messages
from permissions import permission_check


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if (isinstance(error, permission_check.NotAdminError)):
            await inter.response.send_message(error.message, ephemeral=True)
            return

        if (
            isinstance(error, commands.MissingPermissions)
            or isinstance(error, commands.errors.CheckFailure)
        ):
            await inter.response.send_message(Messages.not_enough_perms, ephemeral=True)
            return

        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(
                Messages.command_cooldowns.format(time=round(error.retry_after, 1)))
            return

        if isinstance(error, disnake.InteractionTimedOut):
            await inter.response.send_message(Messages.command_timed_out)
            return

        channel = self.bot.get_channel(config.bot_dev_channel)
        await inter.send(Messages.Lotus_error)
        url = f"https://discord.com/channels/{inter.guild_id}/{inter.channel_id}/{inter.id}"

        output = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        embed = disnake.Embed(title=f"Ignoring exception on command {inter.data.name}", color=0xFF0000)
        embed.add_field(name="Autor", value=str(inter.author))

        if inter.guild and inter.guild.id != config.guild_id:
            embed.add_field(name="Guild", value=inter.guild.name)
        embed.add_field(name="Zpráva", value=inter.filled_options, inline=False)
        embed.add_field(name="Link", value=url, inline=False)

        print(output)
        await channel.send(embed=embed)

        output = utility.cut_string(output, 1900)
        if channel is not None:
            for message in output:
                await channel.send(f"```\n{message}\n```")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if (isinstance(error, permission_check.NotAdminError)):
            await ctx.send(error.message)
            return

        if (
            isinstance(error, commands.MissingPermissions)
            or isinstance(error, commands.errors.CheckFailure)
        ):
            await ctx.send(Messages.not_enough_perms)
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(error)
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(Messages.command_cooldowns.format(time=round(error.retry_after, 1)))
            return

        if isinstance(error, commands.UserInputError):
            await ctx.send(error)
            return

        channel = self.bot.get_channel(config.bot_dev_channel)
        message = await ctx.send(Messages.Lotus_error)

        output = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        embed = disnake.Embed(title=f"Ignoring exception on command {ctx.command}", color=0xFF0000)
        embed.add_field(name="Autor", value=str(ctx.author))

        if ctx.guild and ctx.guild.id != config.guild_id:
            embed.add_field(name="Guild", value=ctx.guild.name)
        embed.add_field(name="Zpráva", value=ctx.message.content[:1000], inline=False)
        embed.add_field(name="Link", value=ctx.message.jump_url, inline=False)

        print(output)
        await channel.send(embed=embed)

        output = utility.cut_string(output, 1900)
        if channel is not None:
            for message in output:
                await channel.send(f"```\n{message}\n```")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        channel_out = self.bot.get_channel(config.bot_dev_channel)
        output = traceback.format_exc()
        print(output)

        embeds = []
        guild = None
        for arg in args:
            if arg.guild_id:
                guild = self.bot.get_guild(arg.guild_id)
                event_guild = guild.name
                channel = guild.get_channel(arg.channel_id)
                message = await channel.fetch_message(arg.message_id)
                message = message.content[:1000]
            else:
                event_guild = "DM"
                message = arg.message_id

            user = self.bot.get_user(arg.user_id)
            if not user:
                user = arg.user_id
            else:
                channel = self.bot.get_channel(arg.channel_id)
                if channel:
                    message = await channel.fetch_message(arg.message_id)
                    if message.content:
                        message = message.content[:1000]
                    elif message.embeds:
                        embeds.extend(message.embeds)
                        message = "Embed v předchozí zprávě"
                    elif message.attachments:
                        message_out = ""
                        for attachment in message.attachments:
                            message_out += f"{attachment.url}\n"
                        message = message_out
                else:
                    message = arg.message_id
                user = str(user)
            embed = Embed(title=f"Ignoring exception on event '{event}'", color=0xFF0000)
            embed.add_field(name="Zpráva", value=message, inline=False)
            if arg.guild_id != config.guild_id:
                embed.add_field(name="Guild", value=event_guild)

        if channel_out is not None:
            output = utility.cut_string(output, 1900)
            for embed in embeds:
                await channel_out.send(embed=embed)
            for message in output:
                await channel_out.send(f"```\n{message}```")


def setup(bot):
    bot.add_cog(Error(bot))
