import json

from parser import builder
from staging import Stage
from stitch import Stitch

if __name__ == "__main__":

    # Build a character profile.
    with open("../profile.json", "r") as f:            # Read in character profile.
        cast = json.load(f)                         # 
        htmlFilePath = '../book/OEBPS/ch01.xhtml'    # Using on chapter for testing.
        exportPath = '../export/'

        buildInstructions = builder(htmlFilePath, cast, exportPath)       # Builder class
        buildInstructions.buildIntructions()                    # Build the instructions for narration.

        instrPath = "../export/Ch01Example.xml"
        staging = Stage(instrPath)
        staging.stage()

        stitch = Stitch()
        stitch.stitchAudio()

        f.close()
