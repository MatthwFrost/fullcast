import json

from parser import builder
from staging import Stage
from stitch import Stitch

if __name__ == "__main__":

    """
    Build process:
    Main - main.py
    Builder - parser.py
    Staging - stage.py
    Stitch - stitch.py

    """

    # Build a character profile.
    with open("../profile.json", "r") as f:            # Read in character profile.
        cast = json.load(f)                         # 
        chapter = "ch01"
        htmlFilePath = f'../book/OEBPS/{chapter}.xhtml'    # Using on chapter for testing.
        exportPath = '../export/'

        buildInstructions = builder(htmlFilePath, cast, exportPath, chapter)       # Builder class
        buildInstructions.buildIntructions()                    # Build the instructions for narration.

        #instrPath = f"../export/{chapter}Instructions.xml" # This can be automated
        #staging = Stage(instrPath, cast)
        #staging.stage()

        #stitch = Stitch()
        #stitch.stitchAudio()

        f.close()
