import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import tickerForDiscord
import ibkrBot
import asyncio

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("we are online")

CheckIfTrue = False

async def printTickersloop(ctx):
    try:
        while CheckIfTrue:
            toPrint = ibkrBot.printTickers()
            await ctx.send(toPrint)
            await asyncio.sleep(3)
    except:
        print("Closing Loop for tickers")

@bot.command()
async def stockticker(ctx, *args):
    global CheckIfTrue
    FirstArg = args[0]
    if FirstArg == "addTicker":
        addtask = bot.loop.create_task(ibkrBot.MarketData(args[1:]))
        await ctx.send(f"Adding tickers: {', '.join(args[1:])}")
    
    elif FirstArg == "LookTicker":
        CheckIfTrue = True
        task = bot.loop.create_task(printTickersloop(ctx))
    
    elif FirstArg == "StopLook":
        CheckIfTrue = False
        await ctx.send("Stopped Printing tickers")

    elif FirstArg == "getTicker":
        await ctx.send(ibkrBot.getTicker())

bot.run(token, log_handler=handler, log_level=logging.DEBUG)