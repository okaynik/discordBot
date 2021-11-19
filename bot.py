import os
from random import randint
import praw
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(client_id=os.getenv('PERSONAL_SCRIPT'),
                     client_secret=os.getenv('SECRET'),
                     user_agent='oke',
                     username=os.getenv('REDDIT_USERNAME'),
                     password=os.getenv('PASSWORD'),
                     check_for_async=False)
subreddit = reddit.subreddit('ProgrammerHumor')

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='+')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

@bot.event
async def on_command_error(ctx, error = 'Something went terribly wrong cause André is annoying'):
    await ctx.send(error)

@bot.command(name='send', help='It shoud send a pic')
async def send_pic(ctx, num = 1):
    if num > 3:
        raise discord.ext.commands.CommandError(message = 'You can only send 3 pics at a time')
    if num == 0:
        ctx.send('Okay')
    if num == -1:
        ctx.send('TODO: Delete last meme')
    if num < -1:
        ctx.send('TODO: Delete last ' + str(abs(num)) + ' memes')
    for _ in range(int(num)):
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
    raise discord.ext.commands.CommandError(message= 'Whoopsie...')

@bot.command(name='wow')
async def ex(ctx):
    raise discord.ext.commands.CommandError(message= 'You\'re beautiful!')

@bot.command(name='random')
async def ex(ctx):
    raise discord.ext.commands.CommandError(message= 'Why are there random commands in here?')

bot.run(TOKEN)