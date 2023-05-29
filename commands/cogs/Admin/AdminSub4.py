import asyncio
import math
import os
import random
import nextcord
from nextcord.ext import commands
import pytz
import requests
import datetime
from sklearn import datasets, model_selection, svm, metrics, linear_model
import joblib
import chess
import chess.svg
import chess.pgn
import random
import os
import time
import csv
from datetime import date
import nextcord, asyncio
from nextcord.ext import commands
from datetime import datetime, timedelta

class FunCommands2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.first_move = True
        self.math_operations = ['+', '-', '*', '/']
        self.black_cards = ["____? There's an app for that.", "Why am I sticky? ____."]
        self.white_cards = [
        "Flying robots that kill people",
        "A man on the brink of orgasm",
        "A passionate Latino lover",
        "A can of whoop-ass",
        "The American Dream",
        "Puppies!",
        "A tiny horse",
        "The Little Engine That Could",
        "Being fabulous",
        "The glass ceiling",
        "The invisible hand",
        "The Great Depression",
        "A pyramid of severed heads",
        "Funky fresh rhymes",
        "A Gypsy curse",
        "A moment of silence",
        "Party poopers",
        "A cooler full of organs",
        "A time travel paradox",
        "Soup that is too hot",
                            ]
        self.active_games = {}
        self.reminders = {}
        
    async def generate_math_problem(self):
        op = random.choice(self.math_operations)
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)

        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        else:
            num1 *= num2  # To avoid floating-point division
            result = num1 // num2

        return f"{num1} {op} {num2}", result
    
    async def create_bug_report_category(self, guild):
        category_name = "🤖・Bug Reports"
        existing_categories = [c.name for c in guild.categories]
        if category_name not in existing_categories:
            return await guild.create_category(category_name)
        else:
            return nextcord.utils.get(guild.categories, name=category_name)

    async def create_bug_report_channel(self, guild):
        bug_report_channel_name = "📁・bug-report-channel"
        existing_channels = [c.name for c in guild.channels]
        if bug_report_channel_name not in existing_channels:
            category = await self.create_bug_report_category(guild)
            return await category.create_text_channel(bug_report_channel_name)
        else:
            return nextcord.utils.get(guild.channels, name=bug_report_channel_name)

    async def create_bug_report(self, interaction):
        user = interaction.user
        guild = interaction.guild
        category = await self.create_bug_report_category(guild)
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        bug_report_channel = await category.create_text_channel(f"bug-report-{user.display_name.lower()}", overwrites=overwrites)
        admin_role = nextcord.utils.get(guild.roles, name="Admin")
        if admin_role:
            await bug_report_channel.set_permissions(admin_role, read_messages=True, send_messages=True)

        await interaction.response.send_message(f"Bug report created: {bug_report_channel.mention}", ephemeral=True)
        await bug_report_channel.send(f"{user.mention}, your bug report has been created. An admin will be with you shortly.\n\n{admin_role.mention} a new bug report has been created by {user.mention}.")
    
    
    

    @nextcord.slash_command()
    async def fun2(self, interaction: nextcord.Interaction):
        """
        This is the main slash command that will be the prefix of all commands below.
        This will never get called since it has subcommands.
        """
        pass

    @fun2.subcommand(description="get a random programming joke2")
    async def progjoke(self, interaction: nextcord.Interaction):
        
        # Fetch a random programming joke from the API
        response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')

        # Extract the joke setup and punchline from the response JSON
        data = response.json()[0]
        setup = data['setup']
        punchline = data['punchline']

        # Send the joke as a message
        await interaction.response.send_message(f'{setup}\n{punchline}')  
        
        
    @fun2.subcommand(description="get a random dad joke2")
    async def quotetext(self, interaction: nextcord.Interaction, text: str):
        
        # Create the quote block
        quote_block = f'```\n{text}\n```'

        # Send the quote block as a message
        await interaction.response.send_message(quote_block)    
    
    @fun2.subcommand( description="reverse a message")
    async def reverse(self, interaction: nextcord.Interaction, message: str):
        # Reverse the message
        reversed_message = message[::-1]

        # Send the reversed message as a code block
        await interaction.response.send_message(f'```\n{reversed_message}\n```')    
        
        
    @fun2.subcommand(description="check message history")
    async def check(self, interaction: nextcord.Interaction, timeframe: int = 7, channel: nextcord.TextChannel = None, *, user: nextcord.Member = None):
        if timeframe > 1968:
            await interaction.channel.send("Sorry. The maximum of days you can check is 1968.")
        elif timeframe <= 0:
            await interaction.channel.send("Sorry. The minimum of days you can check is one.")

        else:
            if not channel:
                channel = interaction.channel
            if not user:
                user = interaction.user

            async with interaction.channel.typing():
                msg = await interaction.channel.send('Calculating...')
                await msg.add_reaction('🔎')

                counter = 0
                async for message in channel.history(limit=5000, after=datetime.today() - timedelta(days=timeframe)):
                    if message.author.id == user.id:
                        counter += 1

                await msg.remove_reaction('🔎', member=message.author)

                if counter >= 5000:
                    await msg.edit(content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
                else:
                    await msg.edit(content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')
        
        
        
        
    @fun2.subcommand(description="get a random space fact")
    async def space_fact(self,interaction: nextcord.Interaction):
        
        response = requests.get("https://api.le-systeme-solaire.net/rest/bodies/")
        if response.status_code == 200:
            planets_data = response.json()["bodies"]
            random_planet = random.choice(planets_data)
            planet_name = random_planet["englishName"]
            planet_fact = f"{planet_name} has a mean radius of {random_planet['meanRadius']} km and an escape velocity of {random_planet['escape']} m/s."
        else:
            planet_fact = "Error fetching space fact, please try again later."

        embed = nextcord.Embed(title="Random Space Fact", description=planet_fact, color=0x00ff00)
        await interaction.response.send_message(embed=embed)
        
    @fun2.subcommand(description="get current time")
    async def time(self, interaction: nextcord.Interaction):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        embed = nextcord.Embed(title="Current Time", description=f"The current time is {current_time}", color=0x00ff00)
        await interaction.response.send_message(embed=embed)    
        
        
        
    @fun2.subcommand(description="get word count")
    async def word_count(self, interaction: nextcord.Interaction, message: str):
        # Count the number of words in the message
        word_count = len(message.split())

        # Send the word count as a code block
        await interaction.response.send_message(f'```\n{word_count}\n```')    
        
    
    @fun2.subcommand(name='update', description='Shows the latest update')
    async def update(self, interaction: nextcord.Interaction):
        with open('update/changelog.md', 'r') as file:
            changelog = file.read()

        embed = nextcord.Embed(title="Changelog", description=changelog, color=0x00FF00)
        await interaction.send(embed=embed)  
        
        
        
    @fun2.subcommand(description="math challenge")
    async def mc(self, interaction: nextcord.Interaction):
        problem, answer = await self.generate_math_problem()
        embed = nextcord.Embed(title="Math Challenge", description=f"Solve this math problem: {problem}")
        await interaction.send(embed=embed)

        def check(m):
            return m.channel == interaction.channel and m.author == interaction.user and not m.author.bot

        try:
            response = await self.bot.wait_for('message', check=check, timeout=20)  # 20 seconds time limit
            if int(response.content) == answer:
                embed = nextcord.Embed(title="Math Challenge", description=f"Correct, {interaction.user.mention}! The answer is {answer}.")
                await interaction.send(embed=embed)
            else:
                embed = nextcord.Embed(title="Math Challenge", description=f"Sorry, {interaction.user.mention}. The correct answer is {answer}.")
                await interaction.send(embed=embed)
        except asyncio.TimeoutError:
            embed = nextcord.Embed(title="Math Challenge", description=f"Time's up! The correct answer was {answer}.")
            await interaction.send(embed=embed)  
            
            
            
    @fun2.subcommand(description="cards against humanity start")
    async def cah_start(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.active_games:
            await interaction.send("A game of Cards Against Humanity is already in progress in this channel.")
            return

        self.active_games[interaction.channel.id] = {
            "players": [interaction.user],
            "black_card": None,
            "white_cards": {}
        }

        await interaction.send("A new game of Cards Against Humanity has started! Type /cah_join to join the game.")

    @fun2.subcommand(description="cards against humanity join")
    async def cah_join(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.active_games:
            await interaction.send("No active Cards Against Humanity game in this channel. Start a game with !cah_start.")
            return

        if interaction.user not in self.active_games[interaction.channel.id]["players"]:
            self.active_games[interaction.channel.id]["players"].append(interaction.user)
            await interaction.send(f"{interaction.user.mention} has joined the game.")
        else:
            await interaction.send("You are already in the game.")

    @fun2.subcommand(description="cards against humanity play")
    async def cah_play(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.active_games:
            await interaction.send("No active Cards Against Humanity game in this channel. Start a game with /cah_start.")
            return

        game = self.active_games[interaction.channel.id]

        if not game["black_card"]:
            game["black_card"] = random.choice(self.black_cards)

        for player in game["players"]:
            cards = random.sample(self.white_cards, 5)
            game["white_cards"][player] = cards
            await player.send(f"Black card: {game['black_card']}\nYour white cards: {', '.join(cards)}")

        await interaction.send(f"Black card: {game['black_card']}")
        await interaction.send("Check your DMs for your white cards. Type !cah_choose [number] to choose a card.")

    @fun2.subcommand(description="cards against humanity choose")
    async def cah_choose(self, interaction: nextcord.Interaction, index: int):
        if interaction.channel.id not in self.active_games:
            await interaction.send("No active Cards Against Humanity game in this channel. Start a game with /cah_start.")
            return

        game = self.active_games[interaction.channel.id]

        if interaction.user not in game["white_cards"]:
            await interaction.send("You are not participating in this round.")
            return

        if index < 1 or index > 5:
            await interaction.send("Invalid card index. Choose a number between 1 and 5.")
            return

        # This part only shows the chosen card, you need to implement voting and determining the winner.
        chosen_card = game["white_cards"][interaction.user][index - 1]
        await interaction.send(f"{interaction.user.mention} chose: {chosen_card}")
        
        
        
        
    @fun2.subcommand(description="remind me")
    async def remind(self, interaction: nextcord.Interaction, message: str, time: str):
        """Set a reminder for a specific time"""
        user = interaction.user
        try:
            timezone = pytz.timezone(str(user.timezone))
        except AttributeError:
            await interaction.send("Please set your timezone using the `!settimezone` command before setting a reminder.")
            return
        try:
            duration = int(time)
            if duration <= 0:
                raise ValueError
        except ValueError:
            await interaction.send("Invalid duration. Please enter a positive integer number of minutes for the reminder time.")
            return
        reminder_time = timezone.localize(nextcord.utils.utcnow() + nextcord.utils.timedelta(minutes=duration))
        self.reminders[user.id] = (message, reminder_time, interaction.channel.id)
        await interaction.send(f"Reminder set for {reminder_time.strftime('%m/%d/%Y %I:%M %p')}.")

        await asyncio.sleep(duration * 60)
        if user.id in self.reminders:
            del self.reminders[user.id]
            channel = self.bot.get_channel(interaction.channel.id)
            await channel.send(f"{user.mention}, {message}")

    @fun2.subcommand(description="View your active reminders")
    async def viewreminders(self, interaction: nextcord.Interaction):
        
        user = interaction.user
        if user.id in self.reminders:
            reminder = self.reminders[user.id]
            message = reminder[0]
            reminder_time = reminder[1].strftime('%m/%d/%Y %I:%M %p')
            channel = self.bot.get_channel(reminder[2])
            await interaction.send(f"Reminder: `{message}` at {reminder_time} in {channel.mention}")
        else:
            await interaction.send("You have no active reminders.")

    @fun2.subcommand(description="Delete an active reminder")
    async def deletereminder(self, interaction: nextcord.Interaction):
        
        user = interaction.user
        if user.id in self.reminders:
            del self.reminders[user.id]
            await interaction.send("Reminder deleted.")
        else:
            await interaction.send("You have no active reminders to delete.")

    @fun2.subcommand(description="Set the user's timezone for reminder scheduling")
    async def settimezone(self, interaction: nextcord.Interaction, timezone: str):
        
        user = interaction.user
        try:
            pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            await interaction.send("Invalid timezone. Please enter a valid timezone in the format 'Area/Location' (e.g., 'US/Eastern').")
            return
        user.timezone = timezone
        await interaction.send(f"Timezone set to {timezone}.")
        
        
        
    @fun2.subcommand(description="8ball")
    async def eightball(self,  interaction: nextcord.Interaction, *, question):
        responses = ['It is certain',
                    'Without a doubt',
                    'You may rely on it',
                    'Yes definitely',
                    'It is decidedly so',
                    'As I see it, yes',
                    'Most likely',
                    'Yes',
                    'Outlook good',
                    'Signs point to yes',
                    'Reply hazy try again',
                    'Better not tell you now',
                    'Ask again later',
                    'Cannot predict now',
                    'Concentrate and ask again',
                    'Don’t count on it',
                    'Outlook not so good',
                    'My sources say no',
                    'Very doubtful',
                    'No']

        message = nextcord.Embed(title="8 Ball", colour=nextcord.Colour.orange())
        message.add_field(name="Question:", value=question, inline=False)
        message.add_field(name="Answer:", value=random.choice(responses), inline=False)
        await interaction.send(embed=message)   
        
        
        
        
        
        
        
    @fun2.subcommand(description="chess puzzle")
    async def chess_puzzle(self, interaction: nextcord.Interaction, min_rating: int, max_rating: int):
        msg = await interaction.send("Searching for a suitable challenge...")
        candidates = []
        with open("data/chess_puzzles.csv", 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                if int(line[3])-(int(line[4])//2)>min_rating and int(line[3])+(int(line[4])//2) < max_rating:
                    candidates.append(line)

        if len(candidates) == 0:
            return await msg.edit(content="No results found! Please try to widen your rating range.")

        puzzle = random.choice(candidates)
        board = chess.Board(fen=puzzle[1])
        counter = 1
        moves = puzzle[2].split(" ")
        board.push_uci(moves[0])

        if board.is_check():
            boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK,
                                       lastmove=board.move_stack[-1],
                                       check=board.king(True if board.turn else False))
        else:
            boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK, lastmove=board.move_stack[-1])
        f = open("board.svg", "w")
        f.write(boardsvg)
        f.close()
        os.system("convert -density 200 board.svg board.png")
        file = nextcord.File("board.png", filename="image.png")
        embed = nextcord.Embed(title=f"Chess Puzzle", color=nextcord.Colour.orange())
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=f"{'White' if board.turn else 'Black'} to move || Puzzle rating: {puzzle[3]}")
        await msg.delete()
        await interaction.send(file=file, embed=embed)

        def check(m):
            global the_message
            if m.author == interaction.author:
                the_message = m.content
                return True

        while True:
            try:
                await self.bot.wait_for('message', check=check, timeout=180)
                if the_message.lower() == "exit" or the_message.lower() == "quit" or the_message.lower() == "resign" or the_message.lower() == "stop" or the_message.lower() == "cancel":
                    return await interaction.send(embed=nextcord.Embed(title=f"Puzzle Cancelled!", color=nextcord.Colour.red()))
                elif the_message.lower() == "board" or the_message.lower() == "show":
                    file = nextcord.File("board.png", filename="image.png")
                    await interaction.send(file=file, embed=embed)
                    continue
                try:
                    copy_board = board.copy()
                    move = board.push_san(the_message)
                    if move.uci() == moves[counter]:
                        if moves[counter] == moves[-1]:
                            if board.is_check():
                                boardsvg = chess.svg.board(board=board,
                                                           orientation=chess.BLACK if board.turn else chess.WHITE,
                                                           lastmove=board.move_stack[-1],
                                                           check=board.king(True if board.turn else False))
                            else:
                                boardsvg = chess.svg.board(board=board,
                                                           orientation=chess.BLACK if board.turn else chess.WHITE,
                                                           lastmove=board.move_stack[-1])
                            f = open("board.svg", "w")
                            f.write(boardsvg)
                            f.close()
                            os.system("convert -density 200 board.svg board.png")
                            file = nextcord.File("board.png", filename="image.png")
                            embed = nextcord.Embed(title=f"Puzzle Complete!", color=nextcord.Colour.orange())
                            embed.set_image(url="attachment://image.png")
                            embed.set_footer(
                                text=f"Puzzle Completed! || Puzzle link: {puzzle[-1]}")
                            return await interaction.send(file=file, embed=embed)

                        counter+=1
                        board.push_uci(moves[counter])
                        counter+=1
                        if board.is_check():
                            boardsvg = chess.svg.board(board=board,
                                                       orientation=chess.WHITE if board.turn else chess.BLACK,
                                                       lastmove=board.move_stack[-1],
                                                       check=board.king(True if board.turn else False))
                        else:
                            boardsvg = chess.svg.board(board=board,
                                                       orientation=chess.WHITE if board.turn else chess.BLACK,
                                                       lastmove=board.move_stack[-1])
                        f = open("board.svg", "w")
                        f.write(boardsvg)
                        f.close()
                        os.system("convert -density 200 board.svg board.png")
                        file = nextcord.File("board.png", filename="image.png")
                        embed = nextcord.Embed(title=f"Correct!", color=nextcord.Colour.orange())
                        embed.set_image(url="attachment://image.png")
                        embed.set_footer(
                            text=f"{'White' if board.turn else 'Black'} to move || Puzzle rating: {puzzle[3]}")
                        await interaction.send(file=file, embed=embed)

                    else:
                        copy_board.push_uci(moves[counter])
                        if copy_board.is_check():
                            boardsvg = chess.svg.board(board=copy_board,
                                                       orientation=chess.BLACK if copy_board.turn else chess.WHITE,
                                                       lastmove=copy_board.move_stack[-1],
                                                       check=copy_board.king(True if copy_board.turn else False))
                        else:
                            boardsvg = chess.svg.board(board=copy_board,
                                                       orientation=chess.BLACK if copy_board.turn else chess.WHITE,
                                                       lastmove=copy_board.move_stack[-1])
                        f = open("board.svg", "w")
                        f.write(boardsvg)
                        f.close()
                        os.system("convert -density 200 board.svg board.png")
                        file = nextcord.File("board.png", filename="image.png")
                        embed = nextcord.Embed(title=f"Incorrect! Best move was:", color=nextcord.Colour.orange())
                        embed.set_image(url="attachment://image.png")
                        embed.set_footer(
                            text=f"Puzzle Failed... || Puzzle link: {puzzle[-1]}")
                        return await interaction.send(file=file, embed=embed)

                except:
                    await interaction.send("Invalid move! Please try again.")

            except asyncio.TimeoutError:
                return await interaction.send(embed=nextcord.Embed(title="Puzzle timeout! Are you there?", color=nextcord.Color.red()))



    @fun2.subcommand(description="Play a chess puzzle against the bot")
    async def chess_challenge(self, interaction: nextcord.Interaction, time_format: str = "3+0", user: nextcord.Member = None):
        if interaction.channel.id != 1087261545739845652:
            return await interaction.send("Please only use this command in the <#836512663612686357> channel.")

        try:
            game_time = int(time_format[0])
            increment = int(time_format[2])
            if len(time_format) != 3 or time_format[1] != "+":
                return await interaction.send(
                "Invalid time format specified. Please use this format `3+2` with the first number being the availabe minutes\nand the number after the + being the increment in seconds (It can be 0 for none).")
        except:
            return await interaction.send(
                "Invalid time format specified. Please use this format `3+2` with the first number being the availabe minutes\nand the number after the + being the increment in seconds (It can be 0 for none).")

        the_author = interaction.author
        channel = interaction.channel
        if user is None:
            embed = nextcord.Embed(title="Chess Battle", color=nextcord.Colour.orange(),
                                  description=f"{the_author.mention} is inviting anyone to a chess battle with the time of {time_format[0]} minutes with {time_format[2]} second increment!\n\nType `accept` now to accept the challenge and begin a game with them.")
        elif user != the_author and not user.bot:
            embed = nextcord.Embed(title="Chess Battle", color=nextcord.Colour.orange(),
                                  description=f"{the_author.mention} is inviting {user.mention} to a chess battle with the time of {time_format[0]} minutes with {time_format[2]} second increment!\n\nType `accept` now to accept the challenge and begin a game with them.")
        else:
            embed = nextcord.Embed(title="You can't invite yourself or a nextcord bot to a chess battle!")

        await channel.send(embed=embed)

        def check(m):
            global black, white
            if not user:
                if m.content.lower() == 'accept' and not m.author.bot and m.channel == channel and m.author != the_author:
                    black = random.choice([m.author, the_author])
                    if the_author == black:
                        white = m.author
                    else:
                        white = the_author
                    return True
            else:
                if m.content.lower() == 'accept' and not m.author.bot and m.author == user and m.channel == channel:
                    black = random.choice([m.author, the_author])
                    if the_author == black:
                        white = m.author
                    else:
                        white = the_author
                    return True

        def game_check(m):
            global the_message
            the_message = m.content
            if m.author == (white if board.turn else black) and m.channel == channel:
                return True

        try:
            await self.bot.wait_for('message', check=check, timeout=60)
            white_time, black_time = game_time * 60, game_time * 60
            board = chess.Board()
            game = chess.pgn.Game()
            game.headers["White"] = white.name
            game.headers["Black"] = black.name
            game.headers["Site"] = "The Fire Army Discord Server"
            today = date.today()
            game.headers["Date"] = today.strftime("%Y.%m.%d")

            boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK)
            f = open("board.svg", "w")
            f.write(boardsvg)
            f.close()
            os.system("convert -density 200 board.svg board.png")
            file = nextcord.File("board.png", filename="image.png")
            embed = nextcord.Embed(title=f"{white} (WHITE) vs {black} (BLACK)", color=nextcord.Colour.orange())
            embed.set_image(url="attachment://image.png")
            if board.turn:
                embed.set_footer(text=f"White to move || White time: {white_time}s")
            else:
                embed.set_footer(text=f"Black to move || Black time: {black_time}s")
            msg = await channel.send(file=file, embed=embed)
            first_move = True
            updater = 1
            while True:
                try:
                    start = time.time()
                    await self.bot.wait_for('message', check=game_check, timeout=1)
                    if the_message.lower() == "board" or the_message.lower() == "show":
                        file = nextcord.File("board.png", filename="image.png")
                        await interaction.send(file=file, embed=embed)
                        continue
                    try:
                        if the_message == "resign":
                            await channel.send(embed=nextcord.Embed(
                                title=f"{white if board.turn else black} resigns! {black if board.turn else white} wins!",
                                color=nextcord.Color.red()))
                            game.headers["Result"] = "0-1" if board.turn else "1-0"
                            return await channel.send(f"Game PGN:\n```{game}```")

                        move = board.push_san(the_message)
                        if board.turn:
                            white_time -= time.time()-start
                            white_time += increment
                        else:
                            black_time -= time.time()-start
                            black_time += increment

                        if first_move:
                            node = game.add_variation(move)
                            first_move = False
                        else:
                            node = node.add_variation(move)

                        updater = 0

                        if board.is_check():
                            boardsvg = chess.svg.board(board=board,
                                                       orientation=chess.WHITE if board.turn else chess.BLACK,
                                                       lastmove=board.move_stack[-1],
                                                       check=board.king(True if board.turn else False))
                        else:
                            boardsvg = chess.svg.board(board=board,
                                                       orientation=chess.WHITE if board.turn else chess.BLACK,
                                                       lastmove=board.move_stack[-1])
                        f = open("board.svg", "w")
                        f.write(boardsvg)
                        f.close()
                        os.system("convert -density 200 board.svg board.png")
                        file = nextcord.File("board.png", filename="image.png")
                        embed = nextcord.Embed(title=f"{white} (WHITE) vs {black} (BLACK)", color=nextcord.Colour.orange())
                        embed.set_image(url="attachment://image.png")
                        if board.turn:
                            embed.set_footer(text=f"White to move || White time: {round(white_time) if white_time > 20 else round(white_time,2)}s")
                        else:
                            embed.set_footer(text=f"Black to move || Black time: {round(black_time) if black_time > 20 else round(black_time,2)}s")
                        msg = await channel.send(file=file, embed=embed)

                        if board.is_game_over():
                            the_result = board.result()
                            if the_result == "1-0":
                                await channel.send(embed=nextcord.Embed(title=f"{white} wins!", color=nextcord.Color.green()))
                            elif the_result == "0-1":
                                await channel.send(embed=nextcord.Embed(title=f"{black} wins!", color=nextcord.Color.green()))
                            else:
                                await channel.send(embed=nextcord.Embed(title=f"It's a draw!", color=nextcord.Color.orange()))

                            game.headers["Result"] = the_result
                            return await channel.send(f"Game PGN:\n```{game}```")
                    except:
                        await channel.send("Invalid move! Please try again.")
                except asyncio.TimeoutError:
                    if board.turn:
                        white_time-=1
                        if white_time <= 0:
                            await channel.send(embed=nextcord.Embed(title=f"{white} timeout, {black} wins!", color=nextcord.Color.red()))
                            game.headers["Result"] = "0-1" if board.turn else "1-0"
                            return await channel.send(f"Game PGN:\n```{game}```")
                        elif updater >= 5:
                            updater = 0
                            embed.set_footer(text=f"White to move || White time: {round(white_time) if white_time > 20 else round(white_time,2)}s")
                            await msg.edit(embed=embed)
                        else:
                            updater+=1
                    else:
                        black_time-=1
                        if black_time <= 0:
                            await channel.send(embed=nextcord.Embed(title=f"{black} timeout, {white} wins!", color=nextcord.Color.red()))
                            game.headers["Result"] = "0-1" if board.turn else "1-0"
                            return await channel.send(f"Game PGN:\n```{game}```")
                        elif updater >= 5:
                            updater = 0
                            embed.set_footer(text=f"Black to move || Black time: {round(black_time) if black_time > 20 else round(black_time,2)}s")
                            await msg.edit(embed=embed)
                        else:
                            updater+=1

        except asyncio.TimeoutError:
            await channel.send(
                embed=nextcord.Embed(title="Challenge timeout. Try again later...", color=nextcord.Color.red()))
            
            
            
            
    @fun2.subcommand(description="shows who is the mentioned user")
    async def whois(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        if not member:  # if member is no mentioned
            member = interaction.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = nextcord.Embed(colour=nextcord.Colour.orange(), timestamp=interaction.created_at,
                              title=str(member))
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user}")

        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await interaction.send(embed=embed)
        
        
        
        
        
        
    @fun2.subcommand(description="Train a machine learning model on the Iris dataset")
    async def train(self, interaction: nextcord.Interaction, model_type: str, dataset: str = "iris"):
        if model_type.lower() not in ['svm', 'logistic_regression']:
            await interaction.send("Currently supported model types: 'svm' and 'logistic_regression'.")
            return

        if dataset.lower() != "iris":
            await interaction.send("Currently, only the 'iris' dataset is supported.")
            return

        # Load the Iris dataset
        iris = datasets.load_iris()
        X_train, X_test, y_train, y_test = model_selection.train_test_split(
            iris.data, iris.target, test_size=0.3, random_state=42
        )

        # Train the selected model
        if model_type.lower() == 'svm':
            clf = svm.SVC(kernel='linear', C=1)
        elif model_type.lower() == 'logistic_regression':
            clf = linear_model.LogisticRegression(max_iter=1000)

        clf.fit(X_train, y_train)

        # Save the trained model
        model_filename = f'{model_type}_iris_model.pkl'
        joblib.dump(clf, model_filename)

        embed = nextcord.Embed(title="Model Trained", description=f"Model '{model_type}' has been trained and saved as '{model_filename}'.")
        await interaction.send(embed=embed)

    @fun2.subcommand(description="Evaluate a trained model")
    async def evaluate(self, interaction: nextcord.Interaction, model_filename: str):
        if not os.path.isfile(model_filename):
            await interaction.send("The specified model file does not exist.")
            return

        # Load the Iris dataset
        iris = datasets.load_iris()
        X_train, X_test, y_train, y_test = model_selection.train_test_split(
            iris.data, iris.target, test_size=0.3, random_state=42
        )

        # Load the trained model
        clf = joblib.load(model_filename)

        # Evaluate the model
        y_pred = clf.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        classification_report = metrics.classification_report(y_test, y_pred, target_names=iris.target_names)

        embed = nextcord.Embed(title="Model Evaluation", description=f"Accuracy: {accuracy:.2f}\n\nClassification report:\n{classification_report}")
        await interaction.send(embed=embed)

    @fun2.subcommand(description="Predict the class of an Iris flower based on its features.")
    async def predict(self, interaction: nextcord.Interaction, model_filename: str, *input_data: float):
        if not os.path.isfile(model_filename):
            await interaction.send("The specified model file does not exist.")
            return

        if len(input_data) != 4:
            await interaction.send("Please provide exactly 4 input features.")
            return

        # Load the Iris dataset
        iris = datasets.load_iris()

        # Load the trained model
        clf = joblib.load(model_filename)

        # Make a prediction
        prediction = clf.predict([input_data])[0]
        predicted_class = iris.target_names[prediction]

        embed = nextcord.Embed(title="Prediction", description=f"Predicted class: {predicted_class} (class index: {prediction})")
        await interaction.send(embed=embed)
        
    @fun2.subcommand(description="Create a bug report channel")
    @commands.has_permissions(administrator=True)
    async def setup_bug_report_system(self, interaction: nextcord.Interaction):
        bug_report_channel = await self.create_bug_report_channel(interaction.guild)
        embed = nextcord.Embed(title="Bug Report", description="Click the button below to open a bug report.")
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label="Report Bug", custom_id="report_bug")
        view = nextcord.ui.View()
        view.add_item(button)
        await bug_report_channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        if interaction.type == nextcord.InteractionType.component:
            if interaction.data["custom_id"] == "report_bug":
                await self.create_bug_report(interaction)
                
                
def setup(bot):
    bot.add_cog(FunCommands2(bot))