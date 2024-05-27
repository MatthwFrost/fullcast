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
    def __init__(self, path, cast) -> None:
        load_dotenv()

        self.path = path
        self.instructions = []
        self.filename = ""
        self.metadata = []
        self.bookname = "bookname"
        self.voiceIDs = {character["name"]: character["voiceID"] for character in cast}
        self.client = ElevenLabs(api_key=os.getenv('ELEVENLABS_KEY'))


    def stage(self) -> None:

        print("Starting staging.")

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                content = file.read()
                file.close()
        except:
            print("STAGING FAILED: Failed to load instructions file.")
            return

        soup = BeautifulSoup(content, features="lxml")
        tags = soup.find_all('p', namespace=False)

        for index, tag in enumerate(tags):

            # Early loop exit for testing
            # TODO: REMOVE WHEN FULLY TESTING
            if index == 30: break

            attrs = tag.attrs
            character = attrs['data-character']
            quote = tag.get_text()
            self.filename = f"../export/audio/audio_clips/{index}_{self.bookname}_{character.replace(' ', '')}.mp3"
            self.fetchAudio(quote, character)

    def fetchAudio(self, text, character):
        # Voice settings will be waited by the emotion.
        if len(text) >= 1:
            print(f"FETCHING AUDIO - {text[:50]}...")
            audio = self.client.generate(
              text=text.replace("\n", "").replace('"', '').strip(),
              voice=Voice(
                  voice_id=self.voiceIDs[character],
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
