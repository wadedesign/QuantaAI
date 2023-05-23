import enum
import os
import dotenv

dotenv.load_dotenv()


class Token(enum.Enum):
    bot = os.getenv("BOT_TOKEN")
    topgg = os.getenv("TOPGG_TOKEN")
    movie = os.getenv("MOVIEDB_API_KEY")
    airi = os.getenv("AIRI_TOKEN")
    weeby = os.getenv("WEEBY") #! get this later the token for the weeby api !

    twitch_client = os.getenv("TWITCH_CLIENT_ID")
    twitch_access = os.getenv("TWITCH_ACCESS_TOKEN")
    twitch_secret = os.getenv("TWITCH_CLIENT_SECRET")


class Var(enum.Enum):

    vote_role = None # the role id for the vote role

    error_logger = 1087261545739845652 # the channel id for the error logger
    guild_logger = 1087261545739845652 # the channel id for the guild logger
    vote_logger = 1086313113462255676   # the channel id for the vote logger
    post_logger = 1087261545739845652 # the channel id for the post logger
    command_logger = 1087261545739845652 # the channel id for the command logger
    connect_logger = 1087261545739845652 # the channel id for the connect logger

    suggestion_logger = 1087261545739845652 # the channel id for the suggestion logger


class Link(enum.Enum):
    bot = "https://discord.com/api/oauth2/authorize?client_id=1072418891680202824&permissions=8&scope=bot%20applications.commands"
    server = "https://discord.gg/A9gxnwgpEN"
    topgg = None # the link for the top.gg page
    banner = None # the link for the banner
