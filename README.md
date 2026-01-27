make a .env file after cloning and have a var name IBKR_ACCOUNT_ID=(your id here)
add a var named DISCORD_TOKEN=("your discord bot token")

you can run either the dockerfile by using:
    docker build -t (img name) .
    docker run -it --rm (img name) bash
    python3 ibkrBot.py
or running on your local host machine by:
    changing "host.docker.internal" to "127.0.0.1" or vice versa to run on your docker
    python3 discordbot.py


Add your stock tickers and make sure you have subscription to the exchange that the ticker is being traded at:
ibkrBot.py -> watchlst
