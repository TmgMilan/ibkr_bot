from ib_insync import *
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

#getting the acc id from your env file
acc_id = os.getenv("IBKR_ACCOUNT_ID")
print(f"Using IBKR ACCOUNT ID: {acc_id}")


#initialize your instance of the TWS
ib = IB()
ib.connect("127.0.0.1", 7496, clientId=0)

#change the watchlst for whatever ticker you want to watch
lstOfMktData = set()
DictOfContracts = {}

#the a way to view its market data
# also i made it async to send message to discord if the ticker isnt real
# need to implement a ibkrs function that checks if the ticker exists and sends it to discord awaiting
async def MarketData(args):
    for ticker in args:
        if ticker not in lstOfMktData:
            lstOfMktData.add(ticker)
    for ticker in lstOfMktData:
        if ticker in DictOfContracts:
            continue
        contractTaskObj = ib.reqMktData(Stock(ticker.upper(), 'SMART', 'USD'), '', False, False)
        DictOfContracts[ticker] = contractTaskObj

#look to print the price every 3 seconds
def printTickers():
    ls = []
    for ticker, contract in DictOfContracts.items():
        ls.append(f"{ticker} - Last price: {contract.last}")
    return '\n'.join(ls)

def getTicker():
    if lstOfMktData:
        return lstOfMktData
    else:
        return "{ }"

def RmTicker(args):
    for ticker in args:
        if ticker in lstOfMktData:
            lstOfMktData.remove(ticker)
        else:
            #need to implement a discord func that ends myself a message
            pass

