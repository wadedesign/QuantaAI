import os
import nextcord
from nextcord.ext import commands





rooms = [
    {
        "description": "Room 1: You see a door with a number lock. There's a hint on the wall.",
        "hint": "The number is the double of 7.",
        "solution": "14",
    },
    {
        "description": "Room 2: There's a door with a letter lock. A hint is written on the wall.",
        "hint": "The letter is the first letter of the alphabet.",
        "solution": "A",
    },
    {
        "description": "Room 3: The door has a color lock. A riddle is carved into the wall.",
        "hint": "Roses are red, violets are...?",
        "solution": "blue",
    },
    {
        "description": "Room 4: A door with a pattern lock shows a sequence of shapes. A hint is inscribed on the floor.",
        "hint": "The sequence is 'Square, Circle, Triangle, ____'.",
        "solution": "Square",
    },
    {
        "description": "Room 5: The door has a word lock. A riddle is written above the door.",
        "hint": "What has keys but can't open locks?",
        "solution": "piano",
    },
    {
        "description": "Room 6: A door with a symbol lock displays a sequence of elements. A hint is etched into the ceiling.",
        "hint": "The sequence is 'Water, Earth, Fire, ____'.",
        "solution": "Air",
    },
    {
        "description": "Room 7: The door has a number lock. A riddle is written on a parchment.",
        "hint": "What is half of 50?",
        "solution": "25",
    },
    {
        "description": "Room 8: A door with a picture lock displays four images. A hint is painted on a canvas.",
        "hint": "The images are a cake, a present, a balloon, and a ____.",
        "solution": "party hat",
    },
    {
        "description": "Room 9: The door has a number lock. A riddle is inscribed on a plaque.",
        "hint": "How many legs does a spider have?",
        "solution": "8",
    },
    {
        "description": "Room 10: A door with a word lock shows an incomplete phrase. A hint is scratched into the doorframe.",
        "hint": "Complete the phrase: 'An apple a day keeps the ____ away.'",
        "solution": "doctor",
    },
    {
    "description": "Room 11: The door has a word lock with a cryptic riddle on an ancient scroll.",
    "hint": "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?",
    "solution": "echo",
    },
]

escape_room_data = {}

async def get_user_data(user_id):
    if user_id not in escape_room_data:
        escape_room_data[user_id] = {
            "current_room": 0,
            "completed": False,
        }
    return escape_room_data[user_id]


def setup(bot):
    @bot.slash_command(name="start", description="Start escape room")
    async def start(interaction: nextcord.Interaction):
        user_data = await get_user_data(interaction.user.id)
        user_data["current_room"] = 0
        user_data["completed"] = False
        await interaction.response.send_message(rooms[user_data["current_room"]]["description"])

    @bot.slash_command(name="hint", description="Get a Hint for the room!")
    async def hint(interaction: nextcord.Interaction):
        user_data = await get_user_data(interaction.user.id)
        if not user_data["completed"]:
            await interaction.response.send_message(rooms[user_data["current_room"]]["hint"])
        else:
            await interaction.response.send_message("You have already completed the escape room.")

    @bot.slash_command(name="answer", description="Provide the answer to the room")
    async def answer(interaction: nextcord.Interaction, user_answer: str):
        user_data = await get_user_data(interaction.user.id)
        if user_data["completed"]:
            await interaction.response.send_message("You have already completed the escape room.")
            return

        if user_answer.lower() == rooms[user_data["current_room"]]["solution"].lower():
            user_data["current_room"] += 1
            if user_data["current_room"] == len(rooms):
                user_data["completed"] = True
                await interaction.response.send_message("Congratulations! You have completed the escape room!")
            else:
                await interaction.response.send_message("Correct! You have advanced to the next room.")
                await interaction.followup.send(rooms[user_data["current_room"]]["description"])
        else:
            await interaction.response.send_message("Incorrect answer. Please try again.")