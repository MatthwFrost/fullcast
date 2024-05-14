from pyparser import builder
import json

if __name__ == "__main__":

    # Build a character profile.
    with open("../profile.json", "r") as f:            # Read in character profile.
        cast = json.load(f)                         # 
        htmlFilePath = '../book/OEBPS/ch01.xhtml'    # Using on chapter for testing.
        exportPath = '../export/'
        build = builder(htmlFilePath, cast, exportPath)       # Builder class
        build.buildIntructions()                    # Build the instructions for narration.
        #build.testOutput()                         # Not implemented

        f.close()
