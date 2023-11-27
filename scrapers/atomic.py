import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_card(card_name, quiet=False, all_grades=False):
    encoded_card_name = urllib.parse.quote_plus(card_name)
    search_url = f"https://www.atomicempire.com/Card/List?txt={encoded_card_name}"
    print(card_name)
    color_s = '--------' in card_name
    if color_s:
        print(card_name)
        return card_name
    response = requests.get(search_url)

    output_text = ""  # String to accumulate results

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='item-row')

        for item in items:
            original_card_title = item.find('h5').text.strip() if item.find('h5') else 'Unknown'
            if "(Not Tournament Legal)" in original_card_title:
                continue

            # Use the original card title in quiet mode
            card_title = card_name if quiet else original_card_title

            # Include set info only if not in quiet mode
            card_set_tag = item.find('a', href=lambda href: href and "set=" in href)
            card_set = card_set_tag.text.strip() if card_set_tag else 'Unknown Set'

            # Handle multiple grade variant
            card_grades = item.find('select', class_='itemid')
            if card_grades:
                options = card_grades.find_all('option')
                for option in options:
                    grade = option.text.strip()
                    price = float(grade.split('- $')[1]) if '- $' in grade else 0
                    if price >= 5 and (all_grades or "SP/NM" not in grade):
                        result = f"{card_title}, Set: {card_set}, Grade: {grade}\n" if not quiet else f"{card_name}, Grade: {grade}\n"
                        output_text += result

            # Handle single grade variant
            else:
                single_grade_price = item.find('strong')
                if single_grade_price:
                    grade = single_grade_price.text.strip()
                    price = float(grade.split('- $')[1]) if '- $' in grade else 0
                    if price >= 5 and (all_grades or "SP/NM" not in grade):
                        result = f"{card_title}, Set: {card_set}, Grade: {grade}\n" if not quiet else f"{card_name}, Grade: {grade}\n"
                        output_text += result
    else:
        print("Failed to retrieve information")

    return output_text.strip()
