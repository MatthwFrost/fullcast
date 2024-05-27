from spacy.matcher import Matcher
from bs4 import BeautifulSoup
import spacy
import re

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
    def __init__(self, path: str, cast: list, exportPath: str, chapter: str) -> None:
        self.path = path
        self.cast = cast
        self.exportPath = exportPath
        self.writeTitle = f"{chapter}Instructions.xml"
        self.nlp = spacy.load("en_core_web_lg") # How does this compare to the sm model?

    def buildIntructions(self) -> None:
        print("Creating instructions")
        characters = self.getAllCharacters()
        chapterText = self.getChapterText()
        doc = self.nlp(chapterText)
        dn = self.fetchDialogueSpeaker(chapterText, doc, characters)
        self.writeOutput(dn)


    def extractDialogue(self, text: str) -> list:
        dialogues = []
        pattern = r'"([^"]*)"(\s*,\s*(he|she|they) (said|replied|asked)[^.]*\.)?' # Not a good solution. Limited. Could move to a better pattern analysis
        for match in re.finditer(pattern, text, re.IGNORECASE):
            dialogue = match.group(0) # What is the 0 for? 
            start, end = match.span()
            # Capturing the speaker directly if mentioned immediately after the dialogue
            speaker_match = re.search(r'\s*,\s*(he|she|they) (said|replied|asked)', match.group(2) if match.group(2) else '', re.IGNORECASE)
            speaker = speaker_match.group(1) if speaker_match else None
            dialogues.append((dialogue, start, end, speaker))
        return dialogues

    def fetchDialogueSpeaker(self, text:  str, doc, characters: list) -> list:
        last_index = 0
        associations = []
        last_speaker = None

        dialogues = self.extractDialogue(text)
        for dialogue, start, end, implicit_speaker in dialogues:
            if start > last_index:
                narration = text[last_index:start].strip()
                if narration:
                    associations.append(("narrator", narration))

            speaker = implicit_speaker
            if not speaker:
                containing_sentence = next((sent for sent in doc.sents if sent.start_char <= start and sent.end_char >= end), None)
                if containing_sentence:
                    for token in containing_sentence:
                        if token.text in characters:
                            speaker = token.text
                            break

            if not speaker and last_speaker:
                speaker = last_speaker

            associations.append((speaker if speaker else "narrator", dialogue.strip('"')))
            last_speaker = speaker  # Update the last speaker only if a speaker was explicitly mentioned
            last_index = end

        if last_index < len(text):
            remaining_narration = text[last_index:].strip()
            if remaining_narration:
                associations.append(("narrator", remaining_narration))

        return associations

    def getEmotion(self) -> None:
        """
        Sentiment analysis? Is there anything else?
        This will be important.
        The wider range of emotions, the better.
        """
        pass

    def writeOutput(self, dn: list) -> None:
        try:
            # Print the results
            with open(self.exportPath + self.writeTitle, "a") as f:
                for index, (name, text) in enumerate(dn):
                    print(index, name, text)
                    character = None
                    if not name == "narrator":
                        character = self.getSpecificCharacter(self.cast, name)
                        if character == None:
                            # Handle unknown characters, could help find new characters
                            print("ERROR WRITING: Couldn't find character.")

                    f.write(f'<p data-character="{character["name"] if character else name}" data-gender="{character["gender"] if character else "m"}" data-emotion="none" index="{index}">{text}</p>\n')

            f.close()
        except ValueError:
            print(f"Couldn't write instructions to {self.exportPath + self.writeTitle}: {ValueError}")
            return

    def getSpecificCharacter(self, cast: dict, name: str) -> dict:
        for character in cast:
            if character.get('name') == name:
                return character
        return None  # Return None if no match is found

    def getAllCharacters(self) -> list:
        return [character["name"] for character in self.cast]

    def getChapterText(self) -> str:
        with open(self.path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, features="xml")
        tags = soup.find_all('p')

        text = ""
        for index, tag in enumerate(tags):
            # Noticed significantly better results when parsing the text like this. 
            text += tag.get_text()
            text = text.replace("\n", " ").strip().lower()
            text = re.sub(r'\s+', ' ', text)

        return text
