import os
import discord
from discord import Intents
from discord.ext import commands


intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('/home/spl1ce/Projetos/Discord Bots/another bot/cogs/'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(token)
