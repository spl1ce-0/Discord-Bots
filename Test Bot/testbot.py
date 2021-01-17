import discord
from discord import Intents
from discord.ext import commands
import random
import csv

intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.messages = True
bot = commands.Bot(command_prefix='.', intents=intents)


class BotData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None

botdata = BotData()


#bot events

@bot.event
async def on_ready():
    print('Test Bot is ready to test itself!')
    await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name='My prefix is "."'))
    bot.reaction_roles = []

@bot.event
async def on_member_join(member):
    if botdata.welcome_channel != None:
        await botdata.welcome_channel.send('Welcome '+ member.mention+'!!!')
    else:
        pass
@bot.event
async def on_member_remove(member):
    if botdata.goodbye_channel != None:
        await botdata.goodbye_channel.send('Goodbye '+member.name+'!!!')
    else:
        pass


@bot.event
async def on_message(message):
    if message.guild is None and message.author != bot.user:
        channel = bot.get_channel(793533724486270976)
        log_embed = discord.Embed(title='DM sent by '+message.author.name, description=message.content, color=0x00b6ff)
        await channel.send(embed=log_embed)

    elif message.content == 'hi':
        emoji = '\U0001F44B'
        await message.add_reaction(emoji)

    elif message.content == 'ok':
        emoji = '\U0001F197'
        await message.add_reaction(emoji)


    await bot.process_commands(message)


#bot commands

@bot.command()
async def set_welcome_channel(ctx, channel_name=None):
    if channel_name != None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                botdata.welcome_channel = channel
                channel_mention = bot.get_channel(channel.id)
                await ctx.channel.send(embed=discord.Embed(title='Set Welcome Channel', description= 'Welcome channel has been set to '+channel_mention.mention, color=0x0097ff))
                await channel.send(embed=discord.Embed(title='Set Welcome Channel', description= 'This is now the welcome channel.', color=0x0097ff))
    else:
        emoji = '\U0000274C'
        await ctx.channel.send(embed=discord.Embed(title='Set Welcome Channel', description=f'{emoji} You did not provide a channel name.',color=0xff0000))

@bot.command()
async def set_goodbye_channel(ctx, channel_name=None):
    if channel_name != None:
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                botdata.goodbye_channel = channel
                channel_mention = bot.get_channel(channel.id)
                await ctx.channel.send(embed=discord.Embed(title='Set Goodbye Channel', description= 'Goodbye channel has been set to '+channel_mention.mention, color=0x0097ff))
                await channel.send(embed=discord.Embed(title='Set Goodbye Channel', description='This is now the goodbye channel.',color=0x0097ff))
    else:
        emoji = '\U0000274C'
        await ctx.channel.send(embed=discord.Embed(title='Set Goodbye Channel', description=f'{emoji} You did not provide a channel name.',color=0xff0000))


@bot.command()
async def hello(ctx):
    embed_message = discord.Embed(description="Hi, " + ctx.author.mention + "!!!", color=0xff0000)
    await ctx.channel.send(embed=embed_message)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    if amount == 0:
        emoji = '\U0000274C'
        embed_message = discord.Embed(name='Clear', title= f"{emoji}   This is how you use the command: ",description=f".clear [number of messages you want to clear]", color=0xff0000)
        await ctx.channel.send(embed=embed_message)
    elif amount > 15:
        emoji = '\U0000274C'
        embed_message = discord.Embed(name='Clear', title=f"{emoji}   You are crazy!", color=0xff0000)
        await ctx.channel.send(embed=embed_message)
    else:
        await ctx.channel.purge(limit=amount+1)
        embed_message = discord.Embed(title="Clear", description= ctx.author.mention+ f' cleared {amount} messages.', color=0x9933ff)
        message = await ctx.channel.send(embed=embed_message)
        await message.delete(delay=10)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        emoji = '\U0000274C'
        embed_message = discord.Embed(description=f"{emoji} You do not have permission to execute such action.", color=0xff0000)
        await ctx.channel.send(embed=embed_message)


@bot.command()
async def joke(ctx):
    with open('/home/spl1ce/Projetos/Discord Bots/Test Bot/jokes.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|', skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
        joke_choice = random.choice(list(reader))
        joke = joke_choice[0]
        embed_message = discord.Embed(name='Test Bot', title='Joke', description=str(joke), color=0xff0000)
        await ctx.channel.send(embed=embed_message)

@bot.command()
async def addjoke(ctx, *, arg=None):
    if ctx.author.id == 345928604057731073:
        if arg != None:
            joke= [arg]
            with open('jokes.csv','a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(joke)
                emoji = '\U00002705'
                await ctx.channel.send(embed=discord.Embed(description=f"{emoji}  Joke added successfully!",color=0x66ff33))
        else:
            emoji = '\U0000274C'
            await ctx.channel.send(embed=discord.Embed(description=f"{emoji} You did not provide any joke.",color=0xff0000))
    else:
        emoji = '\U0000274C'
        await ctx.channel.send(embed=discord.Embed(description=f"{emoji} You do not have permission to execute such action.", color=0xff0000))
@bot.command()
async def dm(ctx, user_id=None, *, arg=None):
    if user_id!=None and arg!=None:
        try:
            user = await bot.fetch_user(user_id)

            message = discord.Embed(title='Message sent by '+ctx.author.name, description=arg)

            await user.send(embed=message)
            await ctx.channel.send(embed=discord.Embed(title='Message sent to ' + user.name))
        except:
            emoji = '\U0000274C'
            await ctx.channel.send(embed=discord.Embed(title=f"{emoji} Couldn't send the message to this user."))
    else:
        emoji = '\U0000274C'
        embed_message = discord.Embed(name='Clear', title=f"{emoji}  This is how you use the command: ",description=f".dm [user id] [message]", color=0xff0000)
        await ctx.channel.send(embed=embed_message)

@bot.command()
async def message(ctx, user_id=None, *, arg=None):
    if user_id!=None and arg!=None:
        try:
            user = await bot.fetch_user(user_id)
            message=arg
            await user.send(message=message)
            await ctx.channel.send(embed=discord.Embed(title='Message sent to ' + user.name))
        except:
            emoji = '\U0000274C'
            await ctx.channel.send(embed=discord.Embed(title=f"{emoji} Couldn't send the message to this user."))
    else:
        emoji = '\U0000274C'
        embed_message = discord.Embed(name='Clear', title=f"{emoji}  This is how you use the command: ",description=f".dm [user id] [message]", color=0xff0000)
        await ctx.channel.send(embed=embed_message)



@bot.command()
async def say(ctx, *, arg=None):
    if arg != None:
        await ctx.message.delete()
        await ctx.channel.send(arg)
    else:
        emoji = '\U0000274C'
        emoji1 = '\U0001F610'
        await ctx.channel.send(embed=discord.Embed(title='Say command', description=f'{emoji} You forgot to tell me what to say {emoji1}.', color=0xff0000))


bot.run('NzgyMjMyMjc1NTU4NDY1NTU3.X8JMkw.gZezXIuWTAJQs7jJLJDdnnb6fLo')
