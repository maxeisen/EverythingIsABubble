import tweepy
import secrets
import stocks
import cryptos
import random
import sched, time
from datetime import datetime

# Authenticate and create Tweepy instance 
auth=tweepy.OAuthHandler(secrets.API_KEY, secrets.API_KEY_SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
bot=tweepy.API(auth)

# Aggregate stock and crypto symbols
symbols=stocks.STOCKS+cryptos.CRYPTOS
symbolsLength=len(symbols)

# Setup timer to Tweet every {frequency} seconds
frequency=900
s=sched.scheduler(time.time, time.sleep)

# Pick a random symbol and tweet that it's a bubble!
def pickSymbolAndTweet(sc):
    now=datetime.now()
    currentTime=now.strftime("%H:%M:%S")
    symbol=symbols[random.randint(0,symbolsLength-1)]
    tweet="$"+symbol+" is a bubble!"
    bot.update_status(tweet)
    print("Tweeted: \""+tweet+"\" at "+currentTime)
    s.enter(frequency, 1, pickSymbolAndTweet, (sc,))

pickSymbolAndTweet(s)
s.run()