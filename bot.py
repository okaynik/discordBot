import os
from random import randint, choice
import praw
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

# Load .env file
load_dotenv()

# Register to Reddit
reddit = praw.Reddit(
    client_id=os.getenv("PERSONAL_SCRIPT"),
    client_secret=os.getenv("SECRET"),
    user_agent="oke",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("PASSWORD"),
    check_for_async=False,
)
# Specify subreddit
subreddit = reddit.subreddit("ProgrammerHumor")

# define discord and openAi keys
TOKEN = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the prefix
bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        print(f"{guild.name} (id: {guild.id})")
        # members = "\n - ".join([member.name for member in guild.members])
        # print(f"Guild Members:\n - {members}")


# Excetion handler
@bot.event
async def on_command_error(
    ctx, error="Something went terribly wrong cause André is annoying"
):
    await ctx.send(error)


# Send a meme from reddit
@bot.command(name="send", help="It shoud send a pic")
async def send_pic(ctx, num=1):
    if num > 3:
        raise discord.ext.commands.CommandError(
            message="You can only send 3 pics at a time"
        )
    elif num == 0:
        await ctx.send("Whatever bruh")
    elif num < 0:
        await ctx.send(f"TODO: Delete last {str(abs(num))} memes")
    else:
        # Choose a random post from the top of this week
        for _ in range(int(num)):
            e = discord.Embed()
            r = randint(1, 100)
            # Really hacky way to get a random post. TODO: make this better
            for post in subreddit.top(time_filter="week", limit=r):
                # Check if post is a picture
                if post.url[8] == "i":
                    title = post.title
                    url = post.url
            e.set_image(url=url)
            await ctx.send(title, embed=e)


# Test exception handler
@bot.command(name="raise", help="Test exception handler")
async def raise_exception(ctx):
    raise discord.ext.commands.CommandError("Whoopsie...")


# GPT-3 question answering
@bot.command(name="q", help='Ask GPT-3 open AI a question, format: +q "<question>"')
async def question(ctx, str=""):
    if str == "":
        await ctx.send('Please enter a question, format: +q "<question>"')
    elif len(str) > 240:
        await ctx.send(
            "Please paraphrase your question to less than 240 characters for the sake of Nikita's GPT-3 budget"
        )
    else:
        response = callGPT3(str)
        if response == "":
            await ctx.send("I am floored, nothing to say...")
        else:
            await ctx.send(response)


def callGPT3(question):
    start_sequence = "\nA: "
    # restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
        engine="davinci",
        prompt=question + start_sequence,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )

    return response.choices[0].text


@bot.command(name="compliment", help="I don't know, something amazing I guess")
async def compliment(ctx):
    await ctx.send("You're beautiful!")


@bot.command(
    name="random", help="Send random comment of a possibly finite amount of comments"
)
async def random_msg(ctx):
    msgs = [
        "Why are there random commands in here?",
        "Yay!",
        "Nikitaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!",
        "Shhhhhhhh, don't tell Andrew",
        "Nikita doesn't have to know",
        "Monkey see, monkey do",
        "Error, just kidding",
        "p ?=? np",
        "Amazing!",
        "Careful, it's hot",
    ]
    await ctx.send(choice(msgs))


@bot.command(name="andre", help="Send mean comment about André")
async def ex1(ctx):
    await ctx.send("André is a terrbole programmer")


@bot.command(name="nikita", help="Send less mean comment about Nikita")
async def ex2(ctx):
    await ctx.send("Nikita is an interesting speller")


@bot.command(
    name="base64_encode", help="Very carfully encodes a given string into base64"
)
async def ex3(ctx, string=""):
    alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    str = ""
    for _ in range((len(string)) * 4 // 3):
        rand = randint(0, len(alph) - 1)
        str += alph[rand]
    await ctx.send(f"Encoded string: {str}")


bot.run(TOKEN)
