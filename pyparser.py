"""
    GOAL:
        Parse the book and output a format like in the example.
        Then we can use this to automatically call the api. 

    Example output:
        <director> Hello, how are you today?</director>
        <narrator>The director said.</narrator>
        <mr-foster>I'm okay! I got a new puppy and I'm exhausted.</mr-foster>
        <narrator>Mr foster sits down and sighs.</narrator>

    What is important info:
        Speaker - Who is speaking
        Quote - What the speaker says
        Emotion - What does the speaker have?

    Problems:
        Code is very slow. I have no idea what the project will look yet 
"""

from bs4 import BeautifulSoup

def parse_html_file(file_path, cast):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, features="xml")
    tag = soup.find_all('p')
    preCharacter = None

    for content in tag:
        text = content.get_text()
        quote = find_quotes(text)
        character = find_character(text, quote, cast, preCharacter)
        if character:
            gender = character["gender"]
            preCharacter = character  # Update previous character
            narratorBefore, narratorAfter = get_narrator_text(text, quote)
            if quote:
                if narratorBefore:
                    print(f"<p data-character=\"narrator\" data-gender=\"{gender}\" emotion=\"none\">{narratorBefore}</p>")

                print(f"<p data-character=\"{character['name']}\" data-gender=\"{gender}\" emotion=\"none\">{quote}</p>")

                if narratorAfter:
                    print(f"<p data-character=\"narrator\" data-gender=\"{gender}\" emotion=\"none\">{narratorAfter}</p>")
        else:
            print(f"<p data-character=\"narrator\" data-gender=\"m\" emotion=\"none\">{text}</p>")
   
def find_quotes(text):
    quote = ""
    inQuotes = False
    for i, char in enumerate(text):
        if char == '"' and (i == 0 or text[i-1] != '\\'):  # Check for non-escaped quotes
            inQuotes = not inQuotes
            quote += char
            continue
        if inQuotes:
            quote += char
    return quote 

def find_character(text, quote, cast, preCharacter):
    text = text.replace(quote, '').lower()

    foundCharacter = None
    firstOccurrence = float('inf')

    for character in cast:
        name_lower = character["name"].lower()  # Ensure case-insensitive matching
        position = text.find(name_lower)
        if position != -1 and position < firstOccurrence:
            foundCharacter = character
            firstOccurrence = position

    return foundCharacter if foundCharacter else preCharacter

def get_narrator_text(text, substring):
    index = text.find(substring)
    
    if index != -1:
        end_index = index + len(substring)
        return text[:index], text[end_index:]
    else:
        return None, None

# Sentiment analysis? Is there anything?
def get_emoiton():
    pass

        
if __name__ == "__main__":
    cast = [
        {"name": "the director", "gender": "m"}, 
        {"name": "mr. foster", "gender": "m"},
        ] # Manually find characters. Yawn
    html_file_path = 'book/OEBPS/ch01.xhtml' # Using on chapter for testing.

    parse_html_file(html_file_path, cast)

