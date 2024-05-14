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
    def __init__(self, path: str, cast: list) -> None:
        self.path = path
        self.cast = cast
        self.writePath = "Ch01Example.xml"

    def buildIntructions(self) -> None:

        with open(self.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            fikle.close()

        # Parse the HTML and then search for all p tags.
        soup = BeautifulSoup(html_content, features="xml")
        tag = soup.find_all('p')
        preCharacter = None

        # Loop through the tags, and get the text inside them.
        for content in tag:
            text = content.get_text()
            quote = self.findQuotes(text)                                           # Find a quote.
            character = self.findCharacter(text, quote, self.cast, preCharacter)    # Find the character speaking.
            narratorBefore, narratorAfter = self.getNarratorText(text, quote)       # Find the narrator speech.
            #emotion = getEmotion()                                                 # Get the character emotion.

            self.writeOutput(quote, character, narratorBefore, narratorAfter, text)

    def findQuotes(self, text: str) -> str:
        # TODO: Doesn't get narrator text between a quote.
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

    def findCharacter(self, text: str, quote: str, cast: list, preCharacter: dict) -> dict:
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

    def getNarratorText(self, text: str, substring: str) -> str:
        index = text.find(substring)
        if index != -1:
            end_index = index + len(substring)
            return text[:index], text[end_index:]
        else:
            return None, None

    def getEmotion(self) -> None:
        """
        Sentiment analysis? Is there anything else?
        This will be important.
        The wider range of emotions, the better.
        """
        pass

    def writeOutput(self, quote: str, character: dict, narratorBefore: str, narratorAfter: str, text: str) -> None:
        # Improve output. Currently primitive.
        # Cast the output to a file with bash, ex python3 main.py > example.html <- Works for now.
        with open(self.writePath, "a") as f:
            if character:
                gender = character["gender"]    # Find the gender
                preCharacter = character        # Update previous character

                if narratorBefore:
                    f.write(f'<p data-character="narrator" data-gender="{gender}" emotion="none">{narratorBefore}</p>')
                if quote:
                    f.write(f'<p data-character="{character["name"]}" data-gender="{gender}" emotion="none">{character["name"]}: {quote}</p>')
                if narratorAfter:
                    f.write(f'<p data-character="narrator" data-gender="{gender}" emotion="none">{narratorAfter}</p>')
            else:
                f.write(f'<p data-character="narrator" data-gender="m" emotion="none">{text}</p>')
        f.close()
