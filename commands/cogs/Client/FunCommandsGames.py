import asyncio
import base64
import datetime
import nextcord
from nextcord.ext import commands
import feedparser
import requests
from datetime import timedelta
from dateutil import parser
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
import random
import string

scheduled_events = dict()



class FunCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="qfun")
    async def fun(self, interaction: nextcord.Interaction):
        """
        This is the main slash command that will be the prefix of all commands below.
        This will never get called since it has subcommands.
        """
        pass

    @fun.subcommand(description="News updates")
    @commands.has_permissions(administrator=True)
    async def send_news(self,interaction: nextcord.Interaction):
        """Send news updates to a specified channel."""
        await interaction.response.defer()
        await interaction.followup.send("Please provide the channel where the news updates should be sent:", ephemeral=True)
        response = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user)
        channel = response.channel_mentions[0]
        
        await interaction.followup.send("Sending news updates to " + channel.mention, ephemeral=True)
        
        feed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
        index = 0

        while True:
            post = feed.entries[index]
            await channel.send(post.title + ": " + post.link)
            index = (index + 1) % len(feed.entries)
            await asyncio.sleep(300) #should be 5 mins before the next news post

    @fun.subcommand(description="Advertise the bot")
    async def advertise_bot(self,interaction: nextcord.Interaction):
        """
        Advertise the bot and its features.
        """
        # Create a message with information about the bot and its features
        message = """
        **Welcome to Wadder!**
        
        Wadder is a powerful and easy-to-use bot that can help you with a wide range of tasks. Here are some of its key features:
        
        - Slash commands for easy access to bot functionality
        - Customizable settings and preferences
        - Integration with third-party APIs for additional functionality
        - Moderation tools to help keep your server safe and secure
        - And much more!
        
        To get started with Wadder, simply invite it to your server and type `/help` to see a list of available commands.
        """

        # Send the advertisement message as a message
        await interaction.response.send_message(message)    
        
        
        
    @fun.subcommand(description="Advertise the user's server")
    async def advertise_server(self,interaction: nextcord.Interaction, message: str):
        """
        Advertise the user's server in a linked channel.

        Args:
        - message (str): The advertisement message to send to the linked channel.
        """
        # Check if the user has permission to use this command
        if not interaction.channel.permissions_for(interaction.user).administrator:
            return await interaction.response.send_message('You must be an administrator to use this command.')

        # Retrieve the main server and the advertisement channel
        main_server = self.bot.get_guild(850958118049677312)
        ad_channel = main_server.get_channel(1024442696527523891) # change to avd channel 

        # Create the invite link with server icon and join button
        invite_link = await interaction.channel.create_invite(
            max_age=0,
            max_uses=0,
            unique=True,
            reason='Server advertisement invite'
        )
        invite_embed = nextcord.Embed(
            title='Join Our Server!',
            url=invite_link.url,
            description=f'Click the "Join" button below to join our server!\n{message}',
            color=nextcord.Color.blurple()
        )
        invite_embed.set_thumbnail(url=interaction.guild.icon.url)
        invite_embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        invite_embed.set_footer(text='Server Advertisement Invite')

        # Send the advertisement message and the invite link to the advertisement channel
        await ad_channel.send(embed=invite_embed)

        # Send a confirmation message to the user
        await interaction.response.send_message('Your advertisement has been sent to the linked channel.')
        
        
        
        
    @fun.subcommand(description="Send news updates to a specified channel.")
    @commands.has_permissions(administrator=True)
    async def send_news(self,interaction: nextcord.Interaction): 
        """Send news updates to a specified channel."""
        await interaction.response.defer()
        await interaction.followup.send("Please provide the channel where the news updates should be sent:", ephemeral=True)
        response = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user)
        channel = response.channel_mentions[0]
        
        await interaction.followup.send("Sending news updates to " + channel.mention, ephemeral=True)
        
        feed = feedparser.parse("http://rss.cnn.com/rss/edition.rss")
        index = 0

        while True:
            post = feed.entries[index]
            await channel.send(post.title + ": " + post.link)
            index = (index + 1) % len(feed.entries)
            await asyncio.sleep(300) #should be 5 mins before the next news post
        
        
        
        
    @fun.subcommand(description="Send Rules")#remove this for its own cog
    @commands.has_permissions(administrator=True)
    async def send_rules_and_verify(self,interaction: nextcord.Interaction):
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) == '✅'

        # Create the embed for the rules
        rules_embed = nextcord.Embed(title="📖 Server Rules", description="Please read and follow the rules below:")

        # Prompt the user to input the rules one by one
        await interaction.response.send_message('Please input the rules one by one. Type "quit" to finish:')
        rules = []
        while True:
            rule = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user)
            if rule.content.lower() == 'quit':
                break
            rules.append(rule.content)

        # Add the rules to the embed
        for i, rule in enumerate(rules):
            rules_embed.add_field(name=f"🔹 Rule {i+1}", value=f"```{rule}```", inline=False)

        # Prompt the user to specify the channel to send the rules to
        await interaction.followup.send('Please specify the channel to send the rules to (mention the channel):')
        channel_input = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel_mentions)
        channel = channel_input.channel_mentions[0]

        # Prompt the user to specify the role to assign to verified users
        await interaction.followup.send('Please specify the role to assign to verified users:')
        role_input = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user)
        role_name = role_input.content
        role = nextcord.utils.get(interaction.guild.roles, name=role_name)

        # Send the rules as an embed to the specified channel
        rules_message = await channel.send(embed=rules_embed)

        # Add the verification check mark
        await rules_message.add_reaction('✅')
        await interaction.followup.send(f'The rules have been sent to {channel.mention}. React with ✅ on the rules message to gain access to other areas of the Discord server.')

        async def on_reaction_add(reaction, user):
            if reaction.message.id == rules_message.id and user != self.bot.user and str(reaction.emoji) == '✅':
                await user.add_roles(role)
                await interaction.channel.send(f'{user.mention} has been verified and now has access to other areas of the server.')

        self.bot.add_listener(on_reaction_add, 'on_reaction_add')
        
        
        
        
    @fun.subcommand(description="Server Info")
    async def serverinfo(self, interaction: nextcord.Interaction):
        # Define the computer animation frames
        animation = [
            "⠋ Gathering server info...",
            "⠙ Gathering server info...",
            "⠹ Gathering server info...",
            "⠸ Gathering server info...",
            "⠼ Gathering server info...",
            "⠴ Gathering server info...",
            "⠦ Gathering server info...",
            "⠧ Gathering server info...",
            "⠇ Gathering server info...",
            "⠏ Gathering server info...",
        ]

        # Send the initial loading message
        loading_message = await interaction.response.send_message("Gathering server info...")

        # Animate the loading message
        for frame in animation:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.1)

        guild = interaction.guild
        embed = nextcord.Embed(title=f"Server Info: {guild.name}", color=0x00ff00)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Server Region", value=str(guild.region).capitalize(), inline=False)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Text Channels", value=f"{len(guild.text_channels):,}")
        embed.add_field(name="Voice Channels", value=f"{len(guild.voice_channels):,}")
        embed.add_field(name="Roles", value=f"{len(guild.roles):,}")
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.set_footer(text=f"Requested by {interaction.user}")
        embed.set_thumbnail(url=guild.icon.url)

        # Update the loading message with the server info embed
        await loading_message.edit(content="Server info", embed=embed)

        
        
        
        
    @fun.subcommand(description="Create a poll")
    @commands.has_permissions(administrator=True)
    async def poll(self,interaction: nextcord.Interaction, time: int, title: str, options: str):
        

        # Check if required parameters are missing
        if not all((time, title, options)):
            await interaction.response.send_message("Please specify the time, title, and options!", ephemeral=True)
            return

        # Parse options from input string
        options = options.split('|')

        # Check if too many options were provided
        MAX_OPTIONS = 6
        if len(options) > MAX_OPTIONS:
            await interaction.response.send_message(f"Maximum number of options is {MAX_OPTIONS}!", ephemeral=True)
            return

        # Calculate poll end time
        end_time = datetime.now() + timedelta(minutes=time)
        formatted_end_time = nextcord.utils.format_dt(end_time, style="T")

        # Create and send embed with poll options
        options_text = "\n".join([f"`{i}.` {option}" for i, option in enumerate(options, start=1)])

        # Define the color for the embed
        EMBED_COLOR = 0x3498db

        embed = nextcord.Embed(color=EMBED_COLOR, title=title)
        embed.add_field(name="Options", value=options_text, inline=False)
        embed.set_footer(text=f"Poll ends at {formatted_end_time}")

        poll_message = await interaction.channel.send(embed=embed)

        # Add reactions to poll message
        for i in range(1, len(options) + 1):
            await poll_message.add_reaction(f"{i}\uFE0F\u20E3")

        # Send confirmation message to user
        await interaction.response.send_message(f"Poll created in {interaction.channel.mention}!", ephemeral=True)
        
        
        
        
        
    @fun.subcommand(description="Create a reminder message")
    async def remind(self,
        interaction: nextcord.Interaction,
        title: str,
        message: str,
        channel: nextcord.TextChannel,
        repeat_hours: int,
        mention: bool = False
    ):
        """
        Set a reminder message to repeat in a set amount of hours.

        Args:
        - title (str): The title of the reminder message.
        - message (str): The message to be included in the reminder.
        - channel (nextcord.TextChannel): The channel to send the reminder in.
        - repeat_hours (int): The number of hours to wait before repeating the reminder message.
        - mention (bool): Whether or not to mention the @everyone role in the reminder message. Defaults to False.
        """
        # Check if the user has permission to set reminders
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You do not have permission to set reminders.")

        # Create the reminder embed
        embed = nextcord.Embed(
            title=title,
            description=message,
            color=0xff0000
        )
        
        # Mention @everyone if requested
        if mention:
            content = "@everyone"
        else:
            content = None
        
        # Send the initial reminder message
        reminder_msg = await channel.send(content=content, embed=embed)
        
        # Send a response to the user
        await interaction.response.send_message(f"Reminder set for {repeat_hours} hours in {channel.mention}!")
        
        # Define a function to repeat the reminder message
        async def repeat_reminder():
            await asyncio.sleep(repeat_hours * 3600) # Wait for the set number of hours
            while True:
                # Send the reminder message
                reminder_msg = await channel.send(content=content, embed=embed)
                await asyncio.sleep(repeat_hours * 3600) # Wait for the set number of hours again
        
        # Start the repeating reminder loop as a background task
        self.bot.loop.create_task(repeat_reminder())
        
        
        
        
    @fun.subcommand(description="Send the rules to a channel")
    @commands.has_permissions(administrator=True)
    async def send_rules(self,interaction: nextcord.Interaction):
        # Check if user is an admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.")
            return
        
        
         # Prompt the user to enter the channel name
        await interaction.response.send_message(content='Please enter the name of the channel you want to send the rules to:')

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        try:
            channel_name = await self.bot.wait_for('message', check=check, timeout=60)
        except nextcord.TimeoutError:
            await interaction.send("You took too long to respond.")
            return

        await interaction.send('Please enter the rules, one by one. Type `done` when you are finished.')

        rules = []
        while True:
            try:
                rule_message = await self.bot.wait_for('message', check=check, timeout=60)
            except nextcord.TimeoutError:
                await interaction.send('You took too long to respond.')
                return

            if rule_message.content.lower() == 'done':
                break

            rules.append(rule_message.content)

        channel = nextcord.utils.get(interaction.guild.channels, name=channel_name.content)

        if channel is None:
            await interaction.send('Channel not found.')
            return

        # Send an embed with the title "Server Rules" and a book icon
        intro_embed = nextcord.Embed(description="📖 Server Rules")
        await channel.send(embed=intro_embed)

        # Send each rule in a separate embed
        for i, rule in enumerate(rules):
            embed = nextcord.Embed(title=f'Rule {i+1}:')
            embed.description = rule
            await channel.send(embed=embed)

        await interaction.send('Rules sent to ' + channel_name.content + '.')
        
        
        
    @fun.subcommand(description="Talk in a channel")
    @commands.has_permissions(administrator=True)
    async def talk(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel, message: str):
        # Define the computer animation frames
        animation = [
            "⠋ Sending message...",
            "⠙ Sending message...",
            "⠹ Sending message...",
            "⠸ Sending message...",
            "⠼ Sending message...",
            "⠴ Sending message...",
            "⠦ Sending message...",
            "⠧ Sending message...",
            "⠇ Sending message...",
            "⠏ Sending message...",
        ]

        # Send the initial loading message with the user as the footer
        embed = nextcord.Embed(description='Calculating...', color=0x00ff00)
        embed.set_footer(text=f"Sent by {interaction.user.name}")
        loading_message = await interaction.response.send_message(embed=embed)

        # Animate the loading message
        for frame in animation:
            embed.description = frame
            await loading_message.edit(embed=embed)
            await asyncio.sleep(0.1)

        # Check if the user has permission to send messages in the specified channel
        if not interaction.user.guild_permissions.manage_messages:
            return await loading_message.edit(content="You do not have permission to send messages in the specified channel.")

        # Send the message to the specified channel
        await channel.send(message)

        # Update the loading message with the completion status
        embed.description = f"Message sent to {channel.mention}!"
        await loading_message.edit(content="Message sent ✅", embed=embed)

        
        
    @fun.subcommand(description="setup welcome and leave messages")
    @commands.has_permissions(administrator=True)
    async def setup(self,interaction: nextcord.Interaction, welcome_message: str, leave_message: str):
        guild = interaction.guild
        welcome_channel = await guild.create_text_channel('🎉welcome')
        leave_channel = await guild.create_text_channel('👋leave')

        async def send_embed(channel, title, color, user, message):
            embed = nextcord.Embed(title=title, color=color)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="Message", value=message)
            await channel.send(embed=embed)

        async def on_member_join(member):
            settings = load_settings(member.guild.id)
            welcome_channel = member.guild.get_channel(settings['welcome_channel'])
            if welcome_channel:
                welcome_msg = f"🎉 {settings['welcome_message']} {member.mention}"
                await send_embed(welcome_channel, f"{member.name} joined the server", 0x00FF00, member, welcome_msg)

        async def on_member_remove(member):
            settings = load_settings(member.guild.id)
            leave_channel = member.guild.get_channel(settings['leave_channel'])
            if leave_channel:
                leave_msg = f"👋 {settings['leave_message']} {member.mention}"
                await send_embed(leave_channel, f"{member.name} left the server", 0xFF0000, member, leave_msg)

        def load_settings(guild_id):
            with open(f'{guild_id}_server_settings.txt', 'r') as f:
                return eval(f.read())

        def save_settings(guild_id, settings):
            with open(f'{guild_id}_server_settings.txt', 'w') as f:
                f.write(str(settings))

        settings = {
            'welcome_channel': welcome_channel.id,
            'leave_channel': leave_channel.id,
            'welcome_message': welcome_message,
            'leave_message': leave_message
        }

        save_settings(guild.id, settings)

        self.bot.add_listener(on_member_join, 'on_member_join')
        self.bot.add_listener(on_member_remove, 'on_member_remove')

        await interaction.response.send_message("Setup complete.", ephemeral=True)
        
    @fun.subcommand(description="Calculate average")
    async def calculate_average(self, interaction: nextcord.Interaction, numbers: str):
        # Define the computer animation frames
        animation = [
            "⠋ Calculating average...",
            "⠙ Calculating average...",
            "⠹ Calculating average...",
            "⠸ Calculating average...",
            "⠼ Calculating average...",
            "⠴ Calculating average...",
            "⠦ Calculating average...",
            "⠧ Calculating average...",
            "⠇ Calculating average...",
            "⠏ Calculating average...",
        ]

        # Send the initial loading message with an embedded message
        embed = nextcord.Embed(title='Average and Sum', color=0x00ff00)
        embed.add_field(name='Average', value='Calculating...', inline=False)
        embed.add_field(name='Sum', value='Calculating...', inline=False)
        loading_message = await interaction.response.send_message(embed=embed)

        # Animate the loading message
        for frame in animation:
            embed.set_field_at(index=0, name='Average', value=frame)
            embed.set_field_at(index=1, name='Sum', value=frame)
            await loading_message.edit(embed=embed)
            await asyncio.sleep(0.1)

        # Convert the comma-separated string of numbers to a list of floats
        numbers_list = [float(n) for n in numbers.split(',')]

        # Calculate the average and sum of the numbers
        average = sum(numbers_list) / len(numbers_list)
        total_sum = sum(numbers_list)

        # Create the final embedded message with the calculated average and sum
        embed.set_field_at(index=0, name='Average', value=f'**Average:** {average:.2f}')
        embed.set_field_at(index=1, name='Sum', value=f'**Sum:** {total_sum:.2f}')

        # Edit the loading message with the final embedded message
        await loading_message.edit(content='Calculation complete ✅', embed=embed)

    
    @fun.subcommand(description="Add two numbers")
    async def add(self, interaction: nextcord.Interaction, num1: int, num2: int):
        # Create an animated loading message
        animation = [
            "⚙️ Calculating result...",
            "⚙️🔢 Calculating result...",
            "⚙️🔢📊 Calculating result...",
            "⚙️🔢📊🔮 Calculating result...",
            "⚙️🔢📊🔮🧮 Calculating result...",
            "⚙️🔢📊🔮🧮🔢 Calculating result...",
        ]
        loading_message = await interaction.response.send_message(animation[0])
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Calculate the sum of the two numbers
        result = num1 + num2

        # Create an embedded message with the result and additional calculations
        embed = nextcord.Embed(title="Addition Result", color=0x00ff00)
        embed.add_field(name="Addition", value=f"The sum of {num1} and {num2} is {result}.")
        embed.add_field(name="Subtraction", value=f"The difference of {num1} and {num2} is {num1 - num2}")
        embed.add_field(name="Multiplication", value=f"The product of {num1} and {num2} is {num1 * num2}")
        embed.add_field(name="Division", value=f"The quotient of {num1} and {num2} is {num1 / num2}")

        # Send the embedded message with the result and calculations
        await loading_message.edit(content="Calculation complete ✅", embed=embed)

    
    @fun.subcommand(description="Convert Celsius to Fahrenheit")
    async def celsius_to_fahrenheit(self, interaction: nextcord.Interaction, celsius: float):
        # Create a cooler animated loading message
        animation = [
            "🌡️ Converting temperature...",
            "🌡️🌞 Converting temperature...",
            "🌡️🌞🌡️ Converting temperature...",
            "🌡️🌞🌡️🌞 Converting temperature...",
            "🌡️🌞🌡️🌞🌡️ Converting temperature...",
            "🌡️🌞🌡️🌞🌡️🌞 Converting temperature...",
            "🌡️🌞🌡️🌞🌡️🌞🌡️ Converting temperature...",
            "🌡️🌞🌡️🌞🌡️🌞🌡️🌞 Converting temperature...",
        ]
        loading_message = await interaction.response.send_message(animation[0])
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Convert the temperature from Celsius to Fahrenheit
        fahrenheit = (celsius * 9/5) + 32

        # Create an embedded message with the converted temperature
        embed = nextcord.Embed(title='Temperature Conversion', color=0x00ff00)
        embed.add_field(name='Celsius', value=f'{celsius}°C', inline=True)
        embed.add_field(name='Fahrenheit', value=f'{fahrenheit}°F', inline=True)

        # Send the embedded message with the converted temperature
        await loading_message.edit(content="Temperature conversion complete ✅", embed=embed)

    
    
    
    @fun.subcommand(description="Get a random Chuck Norris joke")
    async def chucknorris(self, interaction: nextcord.Interaction):
        # Define the computer animation frames
        animation = [
            "🤠 Searching for a Chuck Norris joke...",
            "🤠💪 Looking for Chuck Norris's jokes...",
            "🤠💪👊 Finding the most epic Chuck Norris joke...",
            "🤠💪👊🤣 Generating the perfect Chuck Norris joke...",
            "🤠💪👊🤣🤣 Laughing out loud at Chuck Norris's joke...",
            "🤠💪👊🤣🤣🤠 Chuck Norris approves this joke!",
        ]

        # Create an animated loading message
        loading_message = await interaction.response.send_message(animation[0])
        for frame in animation[1:]:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Fetch a random Chuck Norris joke from the API
        response = requests.get('https://api.chucknorris.io/jokes/random')

        # Extract the joke text from the response JSON
        joke = response.json()['value']

        # Create an embedded message with the joke
        embed = nextcord.Embed(title="Chuck Norris Joke", description=joke, color=0x00ff00)

        # Send the embedded message with the joke
        await loading_message.edit(content="Chuck Norris joke found ✅", embed=embed)

    
    
    
    
    @fun.subcommand(description="Codeblock text")
    async def codeblock(self, interaction: nextcord.Interaction, text: str):
        # Define the computer animation frames
        animation = [
            "```diff\n- Compiling code...\n```",
            "```fix\n- Optimizing code...\n```",
            "```css\n- Running security checks...\n```",
            "```yaml\n- Decrypting secrets...\n```",
            "```diff\n+ Injecting code...\n```",
            "```fix\n+ Exploiting vulnerabilities...\n```",
            "```css\n+ Initiating hacking sequence...\n```",
            "```yaml\n+ Bypassing firewalls...\n```",
            "```diff\n- Analyzing user input...\n```",
            "```fix\n- Detecting bugs...\n```",
            "```css\n- Optimizing performance...\n```",
            "```yaml\n- Debugging...\n```",
            "```diff\n+ Generating artificial intelligence...\n```",
            "```fix\n+ Breaking encryption...\n```",
            "```css\n+ Accessing mainframe...\n```",
            "```yaml\n+ Disabling security protocols...\n```",
        ]

        # Send the initial loading message with an embedded message
        embed = nextcord.Embed(title="Codeblock", description=animation[0], color=0x00ff00)
        loading_message = await interaction.response.send_message(embed=embed)

        # Animate the loading message
        for frame in animation[1:]:
            embed.description = frame

            # Add random color and blinking effect to the codeblock text for each frame
            codeblock_text = f'```diff\n{"".join(["".join(random.choices(string.ascii_letters + string.digits, k=len(c))) for c in text.splitlines()])}```'
            embed.add_field(name="Code", value=codeblock_text, inline=False)

            await loading_message.edit(embed=embed)
            await asyncio.sleep(0.5)

        # Create the final codeblock text with random colors and blinking effect
        codeblock_text = f'```diff\n{"".join(["".join(random.choices(string.ascii_letters + string.digits, k=len(c))) for c in text.splitlines()])}```'

        # Create the embedded message with the codeblock
        embed.description = "Code execution complete!"
        embed.remove_field(0)
        embed.add_field(name="Code", value=codeblock_text, inline=False)

        # Send the embedded message with the codeblock
        await loading_message.edit(embed=embed)
    
    
    
    @fun.subcommand(description="Countdown to a specified event")
    async def countdown(self, interaction: nextcord.Interaction, event_name: str):
        await interaction.response.defer()

        # Create an animated loading message
        animation = [
            "⏳ Calculating the countdown...",
            "⏳⌛ Calculating the countdown...",
            "⏳⌛🔢 Calculating the countdown...",
            "⏳⌛🔢⏰ Calculating the countdown...",
            "⏳⌛🔢⏰📅 Calculating the countdown...",
            "⏳⌛🔢⏰📅🕒 Calculating the countdown...",
        ]
        loading_message = await interaction.followup.send("Calculating the countdown...")
        for frame in animation:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        await interaction.followup.send(f"What's the date and time of the {event_name}? (Please use the following format: YYYY-MM-DD HH:MM)", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        try:
            event_datetime = await self.bot.wait_for('message', check=check, timeout=30.0)
            event_datetime = event_datetime.content.strip()
            event_datetime = parser.parse(event_datetime)
        except nextcord.NotFound:
            await interaction.followup.send("Sorry, I couldn't find your response. Please try again.", ephemeral=True)
            return
        except asyncio.TimeoutError:
            await interaction.followup.send("Sorry, you didn't respond in time. Please try again.", ephemeral=True)
            return
        except ValueError:
            await interaction.followup.send("Sorry, that's not a valid date and time. Please try again.", ephemeral=True)
            return

        now = datetime.utcnow()
        time_diff = event_datetime - now

        days = time_diff.days
        seconds = time_diff.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)

        countdown = f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds until {event_name}!"

        # Create an embedded message with the countdown
        embed = nextcord.Embed(title="Countdown", description=countdown, color=0x00ff00)

        # Send the embedded message with the countdown
        await loading_message.edit(content="Countdown calculated ✅", embed=embed, ephemeral=True)
    
    
    
    @fun.subcommand(description="Get a random dad joke")
    async def dadjoke(self, interaction: nextcord.Interaction):
        try:
            # Create an animated loading message
            animation = [
                "😄 Finding a random dad joke...",
                "😄😂 Finding a random dad joke...",
                "😄😂🤣 Finding a random dad joke...",
                "😄😂🤣😆 Finding a random dad joke...",
                "😄😂🤣😆😁 Finding a random dad joke...",
                "😄😂🤣😆😁😃 Finding a random dad joke...",
            ]
            loading_message = await interaction.response.send_message("Finding a random dad joke...")
            for frame in animation:
                await asyncio.sleep(0.5)
                await loading_message.edit(content=frame)

            # Fetch a random dad joke from the API
            response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'text/plain'})

            print(f"API response: {response.text}")  # Print the response text for debugging

            # Extract the joke text from the response
            joke = response.text

            # Create an embedded message with the joke as the description
            embed = nextcord.Embed(description=joke, color=0xFFFF00)

            # Send the embedded message
            await loading_message.edit(content="Random dad joke found ✅", embed=embed)

        except Exception as error:
            print(f"An error occurred: {error}")
            # Handle the error as per your requirement
    
    
    
    
    
    
    @fun.subcommand(description="Define a word")
    async def define(self, interaction: nextcord.Interaction, word: str):
        try:
            # Create an animated loading message
            animation = [
                "📚 Looking up the definition...",
                "📚🔎 Looking up the definition...",
                "📚🔎📖 Looking up the definition...",
                "📚🔎📖🔍 Looking up the definition...",
                "📚🔎📖🔍📚 Looking up the definition...",
                "📚🔎📖🔍📚🔎 Looking up the definition...",
            ]
            loading_message = await interaction.response.send_message("Looking up the definition...")
            for frame in animation:
                await asyncio.sleep(0.5)
                await loading_message.edit(content=frame)

            url = "https://dictionary-by-api-ninjas.p.rapidapi.com/v1/dictionary"
            querystring = {"word": word}
            headers = {
                "X-RapidAPI-Key": "82cfc7318cmsh3f3e03fa5eb7fdfp16eb9cjsn5bd4ea35cd19",
                "X-RapidAPI-Host": "dictionary-by-api-ninjas.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            print(f"API response: {response.text}")  # Print the response text for debugging

            # Save the response to a text file
            with open("definition.txt", "w") as file:
                file.write(response.text)

            # Create an embedded message to notify the user
            embed = nextcord.Embed(
                title=f"Definition of {word}",
                description="The definition has been sent as a file.",
                color=0x00ff00
            )

            # Send the embedded message
            await loading_message.edit(content="Definition found ✅", embed=embed)

            # Send the file in Discord
            await interaction.followup.send(file=nextcord.File("definition.txt"), content="Here is the definition:")
        
        except Exception as error:
            print(f"An error occurred: {error}")
            # Handle the error as per your requirement
    
    
    @fun.subcommand(name="encode",description="Encode a message in Base64")
    async def encodebase64(self, interaction: nextcord.Interaction, message: str):
        # Create an animated loading message with different animations
        animation = [
            "⌛ Encoding the message.",
            "⏳ Encoding the message..",
            "⌛ Encoding the message..",
            "⏳ Encoding the message...",
            "⌛ Encoding the message...",
            "⏳ Encoding the message....",
        ]
        loading_message = await interaction.response.send_message("Encoding the message.")
        for frame in animation:
            await loading_message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Encode the message in Base64
        encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')

        # Create an embedded message with the encoded message
        embed = nextcord.Embed(title="Base64 Message Encoding", color=0x00ff00)
        embed.add_field(name="Original Message", value=message, inline=False)
        embed.add_field(name="Encoded Message", value=f"```\n{encoded_message}\n```", inline=False)

        # Send the embedded message with the encoded message
        await loading_message.edit(content="Encoding complete ✅", embed=embed)
    
    
    
    
    
    
    @fun.subcommand(name="qencrypt", description="Encrypt a message using the Caesar cipher")
    async def encrypt_caesar(self,
        interaction: nextcord.Interaction,
        text: str,
        shift: int
    ):
        # Convert text to uppercase
        text = text.upper()

        # Define alphabets for encryption
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        shifted_alphabet = alphabet[shift:] + alphabet[:shift]

        # Create an animated loading message
        animation = [
            "🔒 Encrypting the message...",
            "🔒🔐 Encrypting the message...",
            "🔒🔐🔑 Encrypting the message...",
            "🔒🔐🔑🔏 Encrypting the message...",
            "🔒🔐🔑🔏🔒 Encrypting the message...",
            "🔒🔐🔑🔏🔒🔐 Encrypting the message...",
        ]
        message = await interaction.response.send_message("Encrypting the message...")
        for frame in animation:
            await message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Encrypt the text using the Caesar cipher
        encrypted_text = ''
        for char in text:
            if char in alphabet:
                encrypted_text += shifted_alphabet[alphabet.index(char)]
            else:
                encrypted_text += char

        # Create an embedded message with the encrypted text
        embed = nextcord.Embed(title="Caesar Cipher Encryption", color=0x00ff00)
        embed.add_field(name="Original Text", value=text, inline=False)
        embed.add_field(name="Shift", value=shift, inline=False)
        embed.add_field(name="Encrypted Text", value=f"`{encrypted_text}`", inline=False)

        # Send the embedded message with the encrypted text
        await message.edit(content="Encryption complete ✅", embed=embed)
        
    
    
    


    @fun.subcommand(description="Lyrics for a song")
    async def lyrics(self, interaction: nextcord.Interaction, artist: str, song: str):
        # Create an animated loading message
        animation = [
            "🎵 Finding the lyrics...",
            "🎵📡 Finding the lyrics...",
            "🎵📡🔎 Finding the lyrics...",
            "🎵📡🔎🎵 Finding the lyrics...",
            "🎵📡🔎🎵🔎 Finding the lyrics...",
            "🎵📡🔎🎵🔎📡 Finding the lyrics...",
        ]
        message = await interaction.response.send_message("Finding the lyrics...")
        for frame in animation:
            await message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Create an embed with the "We are still working on this" message
        embed = nextcord.Embed(
            title="Lyrics Not Available",
            description="We are still working on this.",
            color=0xFF0000
        )

        # Send the embed as a message
        await message.edit(content="Lyrics not found.")
        await message.edit(embed=embed)



    
    
    
    
    
    
    
    @fun.subcommand(description="Machine learning")
    async def machine_learning(self, interaction: nextcord.Interaction):
        # Ask the user to upload their data
        await interaction.response.send_message("Please upload your data.")

        # Wait for the user to upload their data
        data_message = await self.bot.wait_for("message", check=lambda m: m.author == interaction.author and m.channel == interaction.channel)

        # Train a machine learning model on the data
        await interaction.response.send_message("Training a machine learning model...")

        # Preprocess the data
        data = [data_message.content]
        target = [1]
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(data)

        # Train a support vector machine (SVM) on the data
        clf = svm.SVC(kernel='linear')
        clf.fit(X, target)

        # Send an animated message to prompt for new data
        animation = [
            "🔮 Analyzing...",
            "🔮🔍 Analyzing...",
            "🔮🔍📊 Analyzing...",
            "🔮🔍📊💭 Analyzing...",
            "🔮🔍📊💭🧠 Analyzing...",
            "🔮🔍📊💭🧠🔮 Analyzing..."
        ]
        message = await interaction.response.send_message("Please enter some data to make predictions on...")
        for frame in animation:
            await message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Wait for the user to enter new data to make predictions on
        new_data_message = await self.bot.wait_for("message", check=lambda m: m.author == interaction.author and m.channel == interaction.channel)

        # Preprocess the new data
        new_data = [new_data_message.content]
        X_new = vectorizer.transform(new_data)

        # Make predictions based on the model and the new data
        prediction = clf.predict(X_new)
        if prediction[0] == 1:
            prediction_text = "positive"
        else:
            prediction_text = "negative"

        # Create the embedded message with the prediction
        embed = nextcord.Embed(title=f"🔮 Prediction Result")
        embed.add_field(name="New Data", value=new_data_message.content)
        embed.add_field(name="Prediction", value=f"The prediction is {prediction_text}.")
        embed.set_footer(text="Machine Learning Model")

        # Send the embedded message with the prediction
        await message.edit(content="Prediction complete ✅", embed=embed)

    
    
    
    
    @fun.subcommand(name="qpw",description="generate a random password") #**
    async def generatepassword(self, interaction: nextcord.Interaction, length: int = 16):
        # Generate a random password of the specified length
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Define the embed
        embed = nextcord.Embed(title="Random Password Generator 🔒", color=0x57CFF3)
        embed.add_field(name="Generated Password", value=f'```\n{password}\n```')

        # Define the animation
        animation = [
            "⚡⚡⚡⚡⚡",
            "🔒⚡⚡⚡⚡",
            "🔒🔒⚡⚡⚡",
            "🔒🔒🔒⚡⚡",
            "🔒🔒🔒🔒⚡",
            "🔒🔒🔒🔒🔒"
        ]

        # Send the animated message
        message = await interaction.response.send_message("Generating password...")
        for frame in animation:
            await message.edit(content=frame)
            await asyncio.sleep(0.5)

        # Send the embedded message with the generated password
        await message.edit(content="Password generated ✅", embed=embed)

    
    
    @fun.subcommand(name="qping",description="ping the bot") #**
    async def ping(self, interaction: nextcord.Interaction):
        # Calculate the bot's websocket latency
        latency = self.bot.latency * 1000  # in milliseconds

        # Define the embed
        embed = nextcord.Embed(title="Ping 🏓", color=0xFF5733)
        embed.add_field(name="Latency ⏱️", value=f"{latency:.2f} ms")

        # Define the button to refresh the ping
        async def refresh_callback(interaction: nextcord.Interaction):
            await interaction.response.edit_message(embed=embed)

        # Create the refresh button
        refresh_button = nextcord.ui.Button(label="🔄 Refresh", style=nextcord.ButtonStyle.secondary)
        refresh_button.callback = refresh_callback

        # Create the view and add the refresh button
        view = nextcord.ui.View()
        view.add_item(refresh_button)

        # Send the embed with the refresh button as a response
        await interaction.response.send_message(
            content="**Pinging the Bot** 🌐",
            embed=embed,
            view=view
        )

    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# Don't forget to add the cog to your bot:
# bot.add_cog(FunCommandsCog(bot))
def setup(bot):
    bot.add_cog(FunCommandsCog(bot))