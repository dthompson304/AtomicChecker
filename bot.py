import asyncio
import discord
import nest_asyncio
import os
import random
import pandas as pd

from discord.ext import commands
from scrapers import atomic

anime_responses_search = [
    "OwO what's this? A card search request? On it, Senpai!",
    "Hehe, I'm on the hunt for your cards, Daddy! 🌟",
    "Cards, cards, everywhere! Let me fetch them for you, Teehee! 😊",
    "Hold tight, Senpai! Your card info is coming right up! 🎀",
    "Searching for cards is my favorite! Let's see what I find, UwU!"
]

anime_responses_complete = [
"Yatta! I found all the cards, Senpai! 💖 Are you proud of me? UwU",
"All done, Daddy! Look at all these shiny cards I fetched for you! ✨😊",
"Mission accomplished, Senpai! I hope these cards make you as happy as you make me! 🌸",
"There you go, Daddy! Cards, cards, and more cards! Aren't they kawaii? 🌟🎀",
"Ta-da! Your card search is complete! I worked super hard on it, Teehee! 💫",
"Hehe, I've found everything you asked for, Senpai! I'm such a good bot, aren't I? UwU",
"Look, look, Daddy! I got all the cards! Give me headpats, please? 🐾😻",
"Your card quest is over, Senpai! I hope this brings a big smile to your face! 😄💕",
"Cards galore, just for you, Daddy! I hope they're exactly what you wanted! 🌈🌟",
"All your card dreams have come true, Senpai! I'm so happy to help! 🌟🌙"
]

# Apply nest_asyncio to enable asynchronous operations
nest_asyncio.apply()

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True

#get WD
current_working_directory = os.getcwd()
print("Current Working Directory:", current_working_directory)

# Initialize the Discord bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Global lock variable to prevent command overlap
command_in_progress = False


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='AC')
async def check_cards(ctx, *, card_names):
    global command_in_progress
    if command_in_progress:
        return
    command_in_progress = True

    cringe_mode = '--c' in card_names
    if cringe_mode:
        card_names = card_names.replace('--c', '').strip()

    # Check for quiet mode flag
    quiet_mode = '--q' in card_names
    if quiet_mode:
        card_names = card_names.replace('--q', '').strip()

    if cringe_mode:
        # Select a random response from the anime_responses list
        await ctx.send(random.choice(anime_responses_search))
    else:
        await ctx.send("Request received. Searching for cards...")

    all_grades = '--ag' in card_names
    if all_grades:
        if cringe_mode:
            await ctx.send("Daddy got $$ sending you all in stock options for this card :) :)")
        else:
            await ctx.send("Searching for in stock options for all grades")
        card_names = card_names.replace('--ag', '').strip()
    else:
        if(cringe_mode):
            await ctx.send("We love a daddy who saves his money for me, only checking MP and below grading")
        else:
            await ctx.send("only returning in stock options for grades MP and below")
    try:
        results = []
        if card_names.lower() == 'all':
            if(cringe_mode):
                await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
            else:
                await ctx.send("This is a large request, please be patient")
            file_path = "/root/cards/AtomicChecker/lists/cards.txt"
            with open(file_path, 'r') as file:
                for line in file:
                    card_name = line.strip()
                    if card_name:
                        result = atomic.search_card(card_name, quiet=quiet_mode, all_grades=all_grades)
                        if result:
                            results.append(result.strip())
        else:
            card_names_list = [name.strip() for name in card_names.split(':')]
            list_size = len(card_names_list)
            if list_size > 14:
                if cringe_mode:
                    await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
                else:
                    await ctx.send("This is a large request, please be patient")
            for card_name in card_names_list:
                result = atomic.search_card(card_name, quiet=quiet_mode,  all_grades=all_grades)
                if result:
                    results.append(result.strip())

        if results:
            response = "\n".join(results)
            # Check if response is too long and split if necessary
            while len(response) > 0:
                if len(response) > 2000:
                    part, response = response[:2000], response[2000:]
                    await ctx.send(part)
                else:
                    await ctx.send(response)
                    break
        else:
            await ctx.send("No results found.")


    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        command_in_progress = False
        if cringe_mode:
            # Select a random response from the anime_responses list
            await ctx.send(random.choice(anime_responses_complete))
        else:
            await ctx.send("Search complete thanks for using the bot! ")

bot.run('MTA2NTY0NDQxNDU0Mzg3MjA0MA.GLxxF3.YhqAaXxFhLPrLpKU1pdWkfbrbe0Z8AyobPdxU0')
            
    

#user_input = input("Enter card names separated by commas, or type 'All' for file input: ")
#handle_user_input(user_input)
