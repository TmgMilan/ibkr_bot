import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import database
import ibkrbot
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
    await database.create_db_pool()
    await ibkrbot.conn()

ibkrBot = ibkrbot.ibkrBotClass()
CheckIfTrue = False

async def printTickersloop(ctx):
    try:
        while CheckIfTrue:
            toPrint = await ibkrBot.printTickers(str(ctx.author.id))
            await ctx.send(toPrint)
            await asyncio.sleep(2)
    except:
        print("Closing Loop for tickers")

@bot.command()
async def stockticker(ctx, *args):
    global CheckIfTrue
    FirstArg = args[0]
    if FirstArg == "addTicker":
        addtask = bot.loop.create_task(ibkrBot.addTicker(args[1:], str(ctx.author.id), ctx.author.name))
        failedArgs = await addtask
        await ctx.send(f"Adding tickers: {', '.join(args[1:])}\n{failedArgs}") 

    elif FirstArg == "lookTicker":
        CheckIfTrue = True
        task = bot.loop.create_task(printTickersloop(ctx))
    
    elif FirstArg == "stopLook":
        CheckIfTrue = False
        await ctx.send("Stopped Printing tickers")

    elif FirstArg == "getTickers":
        result = await ibkrBot.getTickers(str(ctx.author.id)) 
        await ctx.send(result)

    elif FirstArg == "removeTicker":
        result = await ibkrBot.deleteTickers(str(ctx.author.id), args[1:])
        if result:
            result = "\n" + result
        await ctx.send(f"Removing Tickers: {','.join(args[1:])}" + result)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
