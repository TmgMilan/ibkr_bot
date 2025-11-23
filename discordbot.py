import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import tickerForDiscord

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

@bot.command()
async def stockticker(ctx, *args):
    if args[0] == "addTicker":
        for i in range(1, len(args)):
            tickerForDiscord.addTicker(args[i])
        await ctx.send(f'added the {args[1:]}')
    elif args[0] == "rmTickers":
        for i in range(1, len(args)):
            tickerForDiscord.deleteTicker(args[i])
            await ctx.send(f'deleted the {args[1:]}')
    elif args[0] == "getTickers":
        await ctx.send(tickerForDiscord.getTicker())

bot.run(token, log_handler=handler, log_level=logging.DEBUG)