import requests
from bs4 import BeautifulSoup
import urllib.parse

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

    return output_text.strip(), price, grade
