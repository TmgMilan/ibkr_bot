import asyncio
from ib_insync import *
import database

ib = IB()
async def conn():
    global ib
    await ib.connectAsync("127.0.0.1", 7496, clientId=1)


class ibkrBotClass:

    async def getUserID(self, discord_id):
        row = await database.pool.fetchrow(
            "SELECT id FROM users WHERE discord_id=$1",
            discord_id
        )
        return row["id"]


    async def addTicker(self, args, discord_id, username):

        await database.pool.execute(
            """
            INSERT INTO users (discord_id, username)
            VALUES ($1, $2)
            ON CONFLICT (discord_id)
            DO UPDATE SET username = EXCLUDED.username
            """,
            discord_id,
            username
        )
       
        user_id = await self.getUserID(discord_id)

        failedToAdd = []
        for arg in args:
            result = await database.pool.execute(
                """
                INSERT INTO stocktickers (user_id, ticker)
                VALUES($1, $2)
                ON CONFLICT DO NOTHING
                """,
                user_id,
                arg
            )
            if result == "INSERT 0 0":
                failedToAdd.append(f'Failed to add {arg}')
            
        return "\n".join(failedToAdd)

    async def getTickers(self, discord_id): 
        user_id = await self.getUserID(discord_id)

        rows = await database.pool.fetch(
            "SELECT ticker FROM stocktickers WHERE user_id=$1",
            user_id
        )

        tickers = [row['ticker'] for row in rows]

        if tickers:
            return tickers
        return "{ }"

    async def printTickers(self, discord_id):
        tickers = await self.getTickers(discord_id)
        lsToPrint = []
        for ticker in tickers:
            contractObj = ib.reqMktData(Stock(ticker, 'SMART', 'USD'), '', False, True)
            await asyncio.sleep(0.5)
        
            lsToPrint.append(f"{ticker} last price - {contractObj.last}, close - {contractObj.close}, bid - {contractObj.bid}")
        return "\n".join(lsToPrint)
    
    async def deleteTickers(self, discord_id, args):
        user_id = await self.getUserID(discord_id)
        failedToDelete = []

        for arg in args:
            result = await database.pool.execute(
                """
                DELETE FROM stocktickers
                Where user_id=$1 AND ticker=$2
                """,
                user_id,
                arg
            )

            if result == "DELETE 0":
                failedToDelete.append(f"This {arg} ticker doesnt exist")

        return "\n".join(failedToDelete)

