from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, save


class Stage:
    """
    Reads the export file. And stages the speech in the correct order, sends it to
    11 labs api, then saves it in the correct locaiton.

    At the moment, i'm not sure if **order** really matters.
    """
    def __init__(self, path) -> None:
        self.path = path
        self.instructions = []
        self.filename = ""
        self.metadata = []
        self.bookname = "bookname"
        self.voiceCharacter = {
            "the director": "UDso2b7nUoYGFzxup38Z",
            "narrator": "cXTSK3LJBx7irlK2jy7q"
        }

        load_dotenv()
        ELEVENLABS_KEY = os.getenv('ELEVENLABS_KEY')
        self.client = ElevenLabs(
          api_key=ELEVENLABS_KEY
        )
        print("Starting staging.")

    def stage(self) -> None:
        """
        Returns list of dicts
        """
        with open(self.path, 'r', encoding='utf-8') as file:
            content = file.read()
            file.close()

        soup = BeautifulSoup(content, features="lxml")
        tags = soup.find_all('p', namespace=False)

        for index, tag in enumerate(tags):

            # Early loop exit for testing
            # TODO: REMOVE WHEN FULLY TESTING
            if index == 15: break

            attrs = tag.attrs
            character = attrs['data-character']
            quote = tag.get_text()
            self.filename = f"../export/audio/{index}_{self.bookname}_{character.replace(' ', '')}.mp3"
            self.fetchAudio(quote, character)

    def fetchAudio(self, text, character):
        # Voice settings will be waited by the emotion.
        if len(text) >= 1:
            print(f"FETCHING AUDIO - {text[:50]}...")
            audio = self.client.generate(
              text=text.replace("\n", "").replace('"', '').strip(),
              voice=Voice(
                  voice_id=self.voiceCharacter[character],
                  settings=VoiceSettings(stability=0.71, similarity_boost=0.6, style=0.6, use_speaker_boost=True)
              ),
              model="eleven_multilingual_v2" # I'm getting weird artifacts.
            )

            self.saveOutput(audio)

    def saveOutput(self, audio):
        """
        Save response from api in an MP3
        """
        save(audio, filename=self.filename)
        print(f"SAVED - {self.filename}")
