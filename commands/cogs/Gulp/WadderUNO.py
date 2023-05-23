import random
import nextcord
from nextcord.ext import commands

class Uno:
    def __init__(self):
        self.deck = self.generate_deck()
        self.player_hand = []
        self.bot_hand = []

    def generate_deck(self):
        colors = ["Red", "Green", "Blue", "Yellow"]
        values = list(range(0, 10)) + ["Skip", "Reverse", "Draw Two"]
        deck = [{"color": c, "value": v} for c in colors for v in values]
        random.shuffle(deck)
        return deck

    def draw_card(self):
        return self.deck.pop()

    def card_value(self, card):
        if isinstance(card["value"], int):
            return card["value"]
        elif card["value"] in ["Skip", "Reverse", "Draw Two"]:
            return 20
        else:  # Wild Card
            return 50

    def hand_value(self, hand):
        value = sum(self.card_value(card) for card in hand)
        return value

class UnoCog2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.uno_games = {}
        
    def hand_to_string(self, hand):
        return ', '.join(self.card_to_string(card) for card in hand)

    def card_to_string(self, card):
        return f"{card['color']} {card['value']}"
    
        
    

    @nextcord.slash_command(name="uno", description="Start a new game of Uno")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="start", description="Start a new game of Uno")
    async def uno_start(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.uno_games:
            await interaction.response.send_message("An Uno game is already in progress in this channel.", ephemeral=True)
            return

        game = Uno()
        self.uno_games[interaction.channel.id] = game

        for _ in range(7):
            game.player_hand.append(game.draw_card())
            game.bot_hand.append(game.draw_card())

        await interaction.response.send_message(f"New Uno game started! Your hand: {self.hand_to_string(game.player_hand)}. Bot's up card: {self.card_to_string(game.bot_hand[0])}")

    @main.subcommand(name="play", description="Play a card in the current Uno game")
    async def uno_play(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.uno_games:
            await interaction.response.send_message("No active Uno game in this channel. Start a game with /uno start.", ephemeral=True)
            return

        # Get the player card from interaction data
        player_card = None
        for option in interaction.data.get('options', []):
            if option['name'] == 'card':
                player_card = option['value'].lower()
                break

        if not player_card:
            await interaction.response.send_message("Please provide a card to play.", ephemeral=True)
            return

        game = self.uno_games[interaction.channel.id]

        if player_card not in game.player_hand:
            await interaction.response.send_message(f"You don't have {player_card} in your hand. Try again.", ephemeral=True)
            return

        player_hand_value = game.hand_value(game.player_hand)
        if player_hand_value > 500:
            del self.uno_games[interaction.channel.id]
            await interaction.response.send_message(f"You played {player_card}. Your hand is now {self.hand_to_string(game.player_hand)}. You win!")
        else:
            await interaction.response.send_message(f"You played {player_card}. Your hand is now {self.hand_to_string(game.player_hand)}.")

    @main.subcommand(name="draw", description="Draw a card in the current Uno game")
    async def uno_draw(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.uno_games:
            await interaction.response.send_message("No active Uno game in this channel. Start a game with /uno start.", ephemeral=True)
            return

        game = self.uno_games[interaction.channel.id]
        game.player_hand.append(game.draw_card())

        player_hand_value = game.hand_value(game.player_hand)
        if player_hand_value > 500:
            del self.uno_games[interaction.channel.id]
            await interaction.response.send_message(f"You drew {self.card_to_string(game.player_hand[-1])}. Your hand is now {self.hand_to_string(game.player_hand)}. You win!")
        else:
            await interaction.response.send_message(f"You drew {self.card_to_string(game.player_hand[-1])}. Your hand is now {self.hand_to_string(game.player_hand)}.")

    @main.subcommand(name="pass", description="Pass your turn in the current Uno game")
    async def uno_pass(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.uno_games:
            await interaction.response.send_message("No active Uno game in this channel. Start a game with /uno start.", ephemeral=True)
            return
        game = self.uno_games[interaction.channel.id]

        bot_hand_value = game.hand_value(game.bot_hand)
        if bot_hand_value > 500:
            del self.uno_games[interaction.channel.id]
            await interaction.response.send_message(f"Bot's hand is now {self.hand_to_string(game.bot_hand)}. Bot wins!")
        else:
            await interaction.response.send_message(f"Bot's hand is now {self.hand_to_string(game.bot_hand)}.") 
            
def setup(bot):
    bot.add_cog(UnoCog2(bot))