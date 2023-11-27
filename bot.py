import asyncio
import discord
import nest_asyncio
import os
import pandas as pd

from discord.ext import commands
from scrapers import atomic

# Apply nest_asyncio to enable asynchronous operations
nest_asyncio.apply()

# Set up Discord intents
intents = discord.Intents.default()
intents.messages = True

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
   
    # Check for quiet mode flag
    quiet_mode = '--q' in card_names
    if quiet_mode:
        await ctx.send("Request received Daddy. Quietly searching for cards ;)...")
        # Remove the --q flag from the input
        card_names = card_names.replace('--q', '').strip()
    else:
        await ctx.send("Request received Daddy. Loud and Proud searching for cards ;)...")

    all_grades = '--ag' in card_names
    if all_grades:
        await ctx.send("Daddy got $$ sending you all stock options for this card :) :)")
        card_names = card_names.replace('--ag', '').strip()
    else:
        await ctx.send("We love a daddy who saves his money for me, only checking MP and below grading")

    try:
        results = []
        if card_names.lower() == 'all':
            await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
            file_path = "Atmoic Checker\lists\cards.txt"
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
                 await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
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
        await ctx.send("Search complete Senpai. I hope youre happy and use me again like the bad bot I am! xoxo <2<3<3")

bot.run('MTE3NjYxODg1MTk2NjkyMjg2Ng.GeBNfd.SUiJf2g3TvzWHc_EO5RXYSj-5EeVsfGYJBBNIM')
            
    

#user_input = input("Enter card names separated by commas, or type 'All' for file input: ")
#handle_user_input(user_input)
