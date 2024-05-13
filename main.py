from pyparser import builder

if __name__ == "__main__":
    # Build a character profile.
    cast = [
        {"name": "the director", "gender": "m", "nationalitly": "british", "features": ["brave", "emotional", "strong-willed"]},
        {"name": "mr. foster", "gender": "m", "nationalitly": "british", "features": ["brave", "emotional", "strong-willed"]},
    ] # Manually find characters. Yawnnn
    html_file_path = 'book/OEBPS/ch01.xhtml'    # Using on chapter for testing.

    build = builder(html_file_path, cast)       # Builder class
    build.buildIntructions()                    # Build the instructions for narration.
    #build.testOutput()                         # Not implemented
