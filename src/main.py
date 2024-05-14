from pyparser import builder
import json

if __name__ == "__main__":

    # Build a character profile.
    with open("profile.json", "r") as f:            # Read in character profile.
        cast = json.load(f)                         # 
        html_file_path = 'book/OEBPS/ch01.xhtml'    # Using on chapter for testing.
        build = builder(html_file_path, cast)       # Builder class
        build.buildIntructions()                    # Build the instructions for narration.
        #build.testOutput()                         # Not implemented

        f.close()
