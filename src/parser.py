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
    def __init__(self, path: str, cast: list, exportPath: str) -> None:
        self.path = path
        self.cast = cast
        self.exportPath = exportPath
        self.writeTitle = "Ch01Example.xml"
        print("Creating instructions")

    def buildIntructions(self) -> None:
        with open(self.path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, features="xml")
        tags = soup.find_all('p')
        self.preCharacter = None

        for index, tag in enumerate(tags):
            text = tag.get_text()
            segments = self.findQuotes(text)

            for segment in segments:
                if segment['type'] == 'quote':
                    character = self.findCharacter(segment, text)
                    self.preCharacter = character
                    self.writeOutput(character, segment['text'], index)
                else:
                    self.writeOutput('narrator', segment['text'], index)

        print("Finished instructions")

    def findQuotes(self, text: str) -> str:
        segments = []
        current_segment = ""
        inQuotes = False
        for i, char in enumerate(text):
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                if inQuotes:
                    current_segment += char
                    segments.append({'type': 'quote', 'text': current_segment.strip()})
                    current_segment = ""
                else:
                    if current_segment:
                        segments.append({'type': 'narrative', 'text': current_segment.strip()})
                        current_segment = ""
                inQuotes = not inQuotes
                current_segment += char
                continue
            current_segment += char

        if current_segment:
            segments.append({'type': 'narrative' if not inQuotes else 'quote', 'text': current_segment.strip()})
        return segments

    def findCharacter(self, segment, text) -> dict:
        if segment['type'] == 'quote':
            foundCharacter = None
            firstOccurrence = float('inf')
            text = text.lower()
            for character in self.cast:
                name_lower = character["name"].lower()
                position = text.find(name_lower)
                if position != -1 and position < firstOccurrence:
                    foundCharacter = character
                    firstOccurrence = position

            return foundCharacter if foundCharacter else (self.preCharacter if self.preCharacter else {'name': 'Unknown'})

        else:
            return self.preCharacter if self.preCharacter else {'name': 'Narrator'}

    def getNarratorText(self, text: str, substring: str) -> str:
        index = text.find(substring)
        if index != -1:
            end_index = index + len(substring)
            return text[:index], text[end_index:]

        return None, None

    def getEmotion(self) -> None:
        """
        Sentiment analysis? Is there anything else?
        This will be important.
        The wider range of emotions, the better.
        """
        pass

    def writeOutput(self, character: dict, text: str, index: int) -> None:
        # Improve output. Currently primitive.
        # Cast the output to a file with bash, ex python3 main.py > example.html <- Works for now.
        with open(self.exportPath + self.writeTitle, "a") as f:
            if character != "narrator":
                gender = character["gender"]    # Find the gender
                name = character["name"]
                f.write(f'<p data-character="{name}" data-gender="{gender}" emotion="none" index="{index}">{text}</p>')
            else:
                f.write(f'<p data-character="narrator" data-gender="m" emotion="none" index="{index}">{text}</p>')
        f.close()

