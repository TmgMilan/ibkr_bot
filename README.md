make a .env file.
add a var named DISCORD_TOKEN=("your discord bot token")
Have your database user named DB_USER, your password DB_PASS, and database name as DB_NAME

You need to have Trader Workstation from Ibkr installed and setup the settings where the port num is 7456 or any free port of your choice as long as you edit it in ibkrbot file.

you can run either the dockerfile by using:
    docker build -t (img name) .
    docker run -it --rm (img name) bash
    python3 ibkrBot.py
or running on your local host machine by:
    changing "host.docker.internal" to "127.0.0.1" or vice versa to run on your docker
    python3 discordbot.py
(currently outdated and can only run on local machine)


Add your stock tickers and make sure you have subscription to the exchange that the ticker is being traded at:
