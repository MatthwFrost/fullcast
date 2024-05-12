from bs4 import BeautifulSoup

class builder:
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
    def __init__(self, path: str, cast: dict):
        self.path = path
        self.cast = cast

    def buildIntructions(self):

        with open(self.path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML and then search for all p tags.
        soup = BeautifulSoup(html_content, features="xml")
        tag = soup.find_all('p')
        preCharacter = None

        # Loop through the p tags, and get the text inside them.
        for content in tag:
            text = content.get_text()

            quote = self.findQuotes(text)                                           # Find a quote.
            character = self.findCharacter(text, quote, self.cast, preCharacter)    # Find the character speaking.
            narratorBefore, narratorAfter = self.getNarratorText(text, quote)       # Find the narrator speech.
            #emotion = getEmotion()                                                 # Get the character emotion.

            # Improve output. Currently primitive.
            if character:
                gender = character["gender"]    # Find the gender
                preCharacter = character        # Update previous character
                if quote:
                    if narratorBefore:
                        print(f"<p data-character=\"narrator\" data-gender=\"{gender}\" emotion=\"none\">{narratorBefore}</p>")

                    print(f"<p data-character=\"{character['name']}\" data-gender=\"{gender}\" emotion=\"none\">{quote}</p>")

                    if narratorAfter:
                        print(f"<p data-character=\"narrator\" data-gender=\"{gender}\" emotion=\"none\">{narratorAfter}</p>")
            else:
                print(f"<p data-character=\"narrator\" data-gender=\"m\" emotion=\"none\">{text}</p>")

    def findQuotes(self, text):
        quote = ""
        inQuotes = False
        for i, char in enumerate(text):
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                inQuotes = not inQuotes # Flips bool: if true, now equals false.
                quote += char # We still want the ""
                continue
            if inQuotes:
                quote += char
        return quote 

    def findCharacter(self, text, quote, cast, preCharacter):
        text = text.replace(quote, '').lower()

        foundCharacter = None
        firstOccurrence = float('inf')

        for character in cast:
            name_lower = character["name"].lower()
            position = text.find(name_lower)
            if position != -1 and position < firstOccurrence:
                foundCharacter = character
                firstOccurrence = position

        return foundCharacter if foundCharacter else preCharacter

    def getNarratorText(self, text, substring):
        index = text.find(substring)
        
        if index != -1:
            end_index = index + len(substring)
            return text[:index], text[end_index:]
        else:
            return None, None

    # Sentiment analysis? Is there anything else?
    # This will be important.
    # The wider range of emotions, the better.
    def getEmotion(self):
        pass
