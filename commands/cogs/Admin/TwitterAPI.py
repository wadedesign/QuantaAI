import nextcord
from nextcord.ext import commands
import tweepy

# Set up Twitter API credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Set up Tweepy API client
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret)
api = tweepy.API(auth)

class TwitterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def tweet(self, *args):
        tweet_text = ' '.join(args)
        try:
            api.update_status(tweet_text)
            await self.bot.say('Tweet posted successfully!')
        except tweepy.TweepError as error:
            await self.bot.say(error.reason)

def setup(bot):
    bot.add_cog(TwitterCog(bot))
