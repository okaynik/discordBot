import os
from random import randint, random
from discord import message
import praw
from itertools import islice
import discord
from discord import embeds
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


reddit = praw.Reddit(client_id=os.getenv('PERSONAL_SCRIPT'),
                     client_secret=os.getenv('SECRET'),
                     user_agent='oke',
                     username=os.getenv('REDDIT_USERNAME'),
                     password=os.getenv('PASSWORD'))
subreddit = reddit.subreddit('ProgrammerHumor')

TOKEN = os.getenv('DISCORD_TOKEN')


# client = discord.Client()
bot = commands.Bot(command_prefix='!')

# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')
#     for guild in client.guilds:
#         break

#     print(f'{guild.name}(id: {guild.id})')

#     members = '\n - '.join([member.name for member in guild.members])
#     print(f'Guild Members:\n - {members}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     print(message.content)
#     if 'say' in message.content.lower():
#         print('logging')
#         #await message.channel.send('Hewwo')
#         await message.channel.send('Hewwo', file=discord.File('https://static.coindesk.com/wp-content/uploads/2021/04/dogecoin-710x458.jpg'))


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send('Something went terribly wrong cause Nikita is a bad programmer')

@bot.command(name='send', help='It shoud send a pic')
async def send_pic(ctx):
    print('smh')
    e = discord.Embed()
    r = randint(1,100)
    for post in subreddit.top('week', limit = r):
        if post.url[8] == 'i':
            title = post.title
            url = post.url
            # print(post.title, post.url)
    e.set_image(url=url)
    await ctx.send(title, embed=e)

@bot.command(name='raise')
async def ex(ctx):
    raise discord.ext.commands.CommandError(message='bad test')


bot.run(TOKEN)