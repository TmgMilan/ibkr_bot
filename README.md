make a .env file after cloning and have a var name "IBKR_ACCOUNT_ID: (your id here)"
you can run either the dockerfile by using:
    docker build -t (img name) .
    docker run -it --rm (img name) bash
    python3 bot.py
or running on your local host machine by:
    changing "host.docker.internal" to "127.0.0.1"
    python3 bot.py
