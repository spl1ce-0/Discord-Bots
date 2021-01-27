from typing import Optional
import discord
from discord import activity
from discord.ext.commands import MemberConverter
from discord.ext.commands import Cog
from discord.ext import commands
from datetime import timezone
from datetime import datetime
from typing import Optional
from discord.ext.commands.errors import MemberNotFound
from discord.member import Member
from discord.utils import get
from discord.webhook import _FriendlyHttpAttributeErrorHelper


class Userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')

    @commands.command()
    async def userinfo(self, ctx, member=None):
        icon='https://cdn.discordapp.com/attachments/792860568285347931/803699182421803098/Logo_do_Bot.png'


        converter = MemberConverter()
        if member != None:
            user= await converter.convert(ctx,member)
        else:
            user=ctx.author
        
        activity = discord.utils.get(user.activities, type=discord.ActivityType.custom)

        permissions = [permission[0] for permission in user.permissions_in(ctx.channel) if permission[1] == True]

        roles=[role for role in user.roles]
        embed = discord.Embed(description=user.mention,
                              color=user.colour or discord.Colour.light_grey,
                              timestamp=datetime.utcnow()
                              )
        

        embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=icon)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',icon_url=ctx.author.avatar_url)
        embed.add_field(name='ID', value=user.id, inline=False)
        embed.add_field(name='Registered', value=user.created_at.strftime(f'%m/%d/%Y | %H:%M:%S UTC'),inline=True)
        embed.add_field(name='Joined', value=user.joined_at.strftime(f'%m/%d/%Y | %H:%M:%S UTC'),inline=True)
        embed.add_field(name='Roles',value=' '.join([role.mention for role in roles]),inline=False)
        embed.add_field(name='Permissions', value=', '.join([str(permission).replace('_',' ').title() for permission in permissions]))
        embed.add_field(name='Status',value=f'Presence: {str(user.raw_status).title()}\n Status: {activity}', inline=False)
        await ctx.channel.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.channel.send(embed=discord.Embed(description='User not found!', colour=discord.Colour.red()))


def setup(bot):
    bot.add_cog(Userinfo(bot))
