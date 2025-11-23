from ib_insync import *
from dotenv import load_dotenv
import os
import tickerForDiscord

load_dotenv()

#getting the acc id from your env file
acc_id = os.getenv("IBKR_ACCOUNT_ID")
print(f"Using IBKR ACCOUNT ID: {acc_id}")


#initialize your instance of the TWS
ib = IB()
ib.connect("host.docker.internal", 7496, clientId=0)

#change the watchlst for whatever ticker you want to watch
watchlst = ["IREN", "DLO"]

#the a way to view its market data
lstOfContracts = [Stock(ticker, 'SMART', 'USD') for ticker in watchlst]
lstOfMktData = [ib.reqMktData(contract, '', False, False) for contract in lstOfContracts]

#look to print the price every 3 seconds
try:
    while True:
        ib.sleep(3)
        for ticker in lstOfMktData:
            print(f"{ticker.contract.symbol} - Last price: {ticker.bid}")
except KeyboardInterrupt:
    print("Disconnecting...")
    ib.disconnect()