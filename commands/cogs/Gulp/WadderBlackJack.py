import random
import nextcord
from nextcord.ext import commands

class Blackjack:
    def __init__(self):
        self.deck = self.generate_deck()
        self.player_hand = []
        self.dealer_hand = []

    def generate_deck(self):
        suits = ["♠", "♥", "♦", "♣"]
        values = list(range(2, 11)) + ["J", "Q", "K", "A"]
        deck = [{"suit": s, "value": v} for s in suits for v in values]
        random.shuffle(deck)
        return deck

    def draw_card(self):
        return self.deck.pop()

    def card_value(self, card):
        if isinstance(card["value"], int):
            return card["value"]
        elif card["value"] in ["J", "Q", "K"]:
            return 10
        else:  # Ace
            return 11

    def hand_value(self, hand):
        value = sum(self.card_value(card) for card in hand)
        aces = sum(card["value"] == "A" for card in hand)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.blackjack_games = {}

    @nextcord.slash_command(name="blackjack", description="Start a new game of Blackjack")
    async def main(self, interaction: nextcord.Interaction):
        pass

    @main.subcommand(name="start", description="Start a new game of Blackjack")
    async def blackjack_start(self, interaction: nextcord.Interaction):
        if interaction.channel.id in self.blackjack_games:
            await interaction.response.send_message("A Blackjack game is already in progress in this channel.", ephemeral=True)
            return

        game = Blackjack()
        self.blackjack_games[interaction.channel.id] = game

        for _ in range(2):
            game.player_hand.append(game.draw_card())
            game.dealer_hand.append(game.draw_card())

        await interaction.response.send_message(f"New Blackjack game started! Your hand: {self.hand_to_string(game.player_hand)}. Dealer's up card: {self.card_to_string(game.dealer_hand[0])}")

    @main.subcommand(name="hit", description="Draw another card in the current Blackjack game")
    async def blackjack_hit(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.blackjack_games:
            await interaction.response.send_message("No active Blackjack game in this channel. Start a game with /blackjack start.", ephemeral=True)
            return

        game = self.blackjack_games[interaction.channel.id]
        game.player_hand.append(game.draw_card())

        player_hand_value = game.hand_value(game.player_hand)
        if player_hand_value > 21:
            del self.blackjack_games[interaction.channel.id]
            await interaction.response.send_message(f"You drew {self.card_to_string(game.player_hand[-1])}. Your hand is now {self.hand_to_string(game.player_hand)}. Busted! You lose.")
        else:
            await interaction.response.send_message(f"You drew {self.card_to_string(game.player_hand[-1])}. Your hand is now {self.hand_to_string(game.player_hand)}.")

    @main.subcommand(name="stand", description="Stand with your current hand in the Blackjack game")
    async def blackjack_stand(self, interaction: nextcord.Interaction):
        if interaction.channel.id not in self.blackjack_games:
            await interaction.response.send_message("No active Blackjack game in this channel. Start a game with /blackjack start.", ephemeral=True)
            return
        game = self.blackjack_games[interaction.channel.id]

        # Dealer draws cards until they have at least 17 points
        while game.hand_value(game.dealer_hand) < 17:
            game.dealer_hand.append(game.draw_card())

        player_hand_value = game.hand_value(game.player_hand)
        dealer_hand_value = game.hand_value(game.dealer_hand)

        if dealer_hand_value > 21 or player_hand_value > dealer_hand_value:
            result = "You win!"
        elif player_hand_value == dealer_hand_value:
            result = "It's a tie!"
        else:
            result = "You lose!"

        del self.blackjack_games[interaction.channel.id]
        await interaction.response.send_message(f"You stand with {self.hand_to_string(game.player_hand)}. Dealer's hand: {self.hand_to_string(game.dealer_hand)}. {result}")

    def card_to_string(self, card):
        return f"{card['value']}{card['suit']}"

    def hand_to_string(self, hand):
        return ", ".join(self.card_to_string(card) for card in hand)
    
    
def setup(bot):
    bot.add_cog(BlackjackCog(bot))