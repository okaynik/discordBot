import os
from random import randint
import praw
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()

reddit = praw.Reddit(client_id=os.getenv('PERSONAL_SCRIPT'),
                     client_secret=os.getenv('SECRET'),
                     user_agent='oke',
                     username=os.getenv('REDDIT_USERNAME'),
                     password=os.getenv('PASSWORD'),
                     check_for_async=False)
subreddit = reddit.subreddit('ProgrammerHumor')

TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = commands.Bot(command_prefix='+')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')


@bot.event
async def on_command_error(ctx, error='Something went terribly wrong cause André is annoying'):
    await ctx.send(error)


@bot.command(name='send', help='It shoud send a pic')
async def send_pic(ctx, num = 1):
    if num > 9 and palindrome(num):
        await ctx.send('Palindrome!')
    elif num > 10000000:
        await ctx.send('Are you trying to crash discord?')

    if num > 3:
        raise discord.ext.commands.CommandError(
            message='You can only send 3 pics at a time')
    elif num == 0:
        await ctx.send('Okay')
    elif num == -1:
        await ctx.send('TODO: Delete last meme')
    elif num < -1:
        await ctx.send('TODO: Delete last ' + str(abs(num)) + ' memes')
    else:
        for _ in range(int(num)):
            e = discord.Embed()
            r = randint(1, 100)
            for post in subreddit.top('week', limit=r):
                if post.url[8] == 'i':
                    title = post.title
                    url = post.url
                    # print(post.title, post.url)
            e.set_image(url=url)
            await ctx.send(title, embed=e)


@bot.command(name='raise', help='Wouldn\'t that be nice')
async def ex1(ctx):
    await ctx.send('Whoopsie...')


@bot.command(name='wow', help='I don\'t know, something amazing I guess')
async def ex2(ctx):
    await ctx.send('You\'re beautiful!')


@bot.command(name='bye', help='Takes down the internet')
async def ex3(ctx):
    await ctx.send('Have a nice day!')


@bot.command(name='random', help='Send random comment of a possibly finite amount of comments')
async def ex4(ctx):
    strs = ['Why are there random commands in here?',
            'Yay!',
            'Nikitaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!',
            'Shhhhhhhh, don\'t tell Andrew',
            'Nikita doesn\'t have to know',
            'Monkey see, monkey do',
            'Error, just kidding',
            'p ?=? np',
            'Amazing!',
            'Careful, it\'s hot']
    rand = randint(0, len(strs) - 1)
    await ctx.send(strs[rand])


@bot.command(name='andre', help='Send mean comment about Andre')
async def ex5(ctx):
    await ctx.send('Andre is a terrbole programmer')


@bot.command(name='Nikita', help='Send less mean comment about Nikita')
async def ex6(ctx):
    await ctx.send('@Nikita is an interesting speller')


@bot.command(name='base64_encode', help='Very carfully encodes a given string into base64')
async def ex7(ctx, string=''):
    alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    str = ''
    for _ in range((len(string))*4//3):
        rand = randint(0, len(alph) - 1)
        str += alph[rand]
    await ctx.send(f'Encoded string: {str}')


@bot.command(name='+', help='Just try it, actually don\'t')
async def ex8(ctx):
    await ctx.send('Ooooooh, the double plus')


@bot.command(name='sned', help='Type faster')
async def ex9(ctx):
    await ctx.send('Bruh')


@bot.command(name='q', help='Ask GPT-3 open AI a question, format: +q "<question>"')
async def ex10(ctx, str = ""):
    if str == "":
        await ctx.send('Please enter a question, format: +q "<question>"')
    elif len(str) > 240:
        await ctx.send('Please paraphrase your question to less than 240 characters for the sake of Nikita\'s GPT-3 budget')
    else:
        response = callGPT3(str)
        if response == "":
            await ctx.send("I am floored, nothing to say...")
        else:
            await ctx.send(response)


def callGPT3(question):
    start_sequence = "\nA: "
    restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
        engine="davinci",
        prompt = question + start_sequence,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )

    return response.choices[0].text


def palindrome(num):
    temp=num
    rev=0
    while(num>0):
        dig=num%10
        rev=rev*10+dig
        num=num//10
    return (temp == rev)

bot.run(TOKEN)