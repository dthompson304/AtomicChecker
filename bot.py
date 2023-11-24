import asyncio
import discord
import nest_asyncio
import pandas as pd

from discord.ext import commands
from scrapers import atomic

# Apply nest_asyncio to enable asynchronous operations
nest_asyncio.apply()

# Set up Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

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

    try:
        results = []
        if card_names.lower() == 'all':
            await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
            file_path = 'lists/cards.txt'
            with open(file_path, 'r') as file:
                for line in file:
                    card_name = line.strip()
                    if card_name:
                        result = atomic.search_card(card_name, quiet=quiet_mode)
                        if result:
                            results.append(result.strip())
        else:
            card_names_list = [name.strip() for name in card_names.split(':')]
            list_size = len(card_names_list)
            if list_size > 14:
                 await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
            for card_name in card_names_list:
                result = atomic.search_card(card_name, quiet=quiet_mode)
                if result:
                    results.append(result.strip())

        if results:
            response = "\n".join(results)
            await ctx.send(response)
        else:
            await ctx.send("No results found.")

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        command_in_progress = False
        await ctx.send("Search complete Senpai. I hope youre happy and use me again like the bad bot I am! xoxo <2<3<3")


async def watchdog(ctx):
    await bot.wait_until_ready()
    
    while not bot.is_closed():
        try:
            results = []

            # Get Card Metadata
            cards_df = pd.read_csv('lists/cards_v2.csv', header=True)
            cards_dicts = cards_df.to_dict('records')

            # Loop and check to see if card is below threshold
            for cards_dict in cards_dicts:
                result, price, grade = atomic.search_card(cards_dict['name'])
                if result and cards_dict['grade'] in grade and price <= cards_dict['threshold']:
                    results.append(result.strip())

            if results:
                response = "\n".join(results)
                await ctx.send('🚨 I found something you might like Senpai.. are you proud of me? 🚨\n' + response)

        except Exception as e:
            print(f"Error: {e}")

        # Wait until next scrape
        await asyncio.sleep(2 * 60 * 60) # 2 hours


bot.loop.create_task(watchdog())
bot.run('')
            
    

#user_input = input("Enter card names separated by commas, or type 'All' for file input: ")
#handle_user_input(user_input)
