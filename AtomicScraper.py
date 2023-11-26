import requests
from bs4 import BeautifulSoup
import urllib.parse
import discord
from discord.ext import commands
import nest_asyncio

def search_card(card_name, quiet=False):
    encoded_card_name = urllib.parse.quote_plus(card_name)
    search_url = f"https://www.atomicempire.com/Card/List?txt={encoded_card_name}"
    response = requests.get(search_url)

    output_text = ""  # String to accumulate results

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='item-row')

        for item in items:
            original_card_title = item.find('h5').text.strip() if item.find('h5') else 'Unknown'
            if "(Not Tournament Legal)" in original_card_title:
                continue

            card_grades = item.find('select', class_='itemid')
            if card_grades:
                options = card_grades.find_all('option')
                for option in options:
                    grade = option.text.strip()
                    if "SP/NM" not in grade:
                        price = float(grade.split('- $')[1]) if '- $' in grade else 0
                        if price >= 5:
                            # Use the original card title in quiet mode
                            card_title = card_name if quiet else original_card_title
                            # Include set info only if not in quiet mode
                            if not quiet:
                                card_set_tag = item.find('a', href=lambda href: href and "set=" in href)
                                card_set = card_set_tag.text.strip() if card_set_tag else 'Unknown Set'
                                result = f"{card_title}, Set: {card_set}, Grade: {grade}\n"
                            else:
                                result = f"{card_name}, Grade: {grade}\n"
                            print(result, end='')
                            output_text += result

    else:
        print("Failed to retrieve information")

    return output_text.strip()



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
            file_path = 'urls.txt'  # Replace with your file path
            with open(file_path, 'r') as file:
                for line in file:
                    card_name = line.strip()
                    if card_name:
                        result = search_card(card_name, quiet=quiet_mode)
                        if result:
                            results.append(result.strip())
        else:
            card_names_list = [name.strip() for name in card_names.split(':')]
            list_size = len(card_names_list)
            if list_size > 15:
                 await ctx.send("You have a big request daddy, please wait for me patiently xoxo")
            for card_name in card_names_list:
                result = search_card(card_name, quiet=quiet_mode)
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
        await ctx.send("Search complete Senpai. I hope youre happy and use me again like the bad bot I am! xoxo <3<3<3")

bot.run('')
            
    

#user_input = input("Enter card names separated by commas, or type 'All' for file input: ")
#handle_user_input(user_input)
