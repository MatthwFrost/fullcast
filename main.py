from pyparser import builder

if __name__ == "__main__":
    cast = [
        {"name": "the director", "gender": "m"}, 
        {"name": "mr. foster", "gender": "m"},
        ] # Manually find characters. Yawnnn
    html_file_path = 'book/OEBPS/ch01.xhtml' # Using on chapter for testing.

    build = builder(html_file_path, cast)
    build.buildIntructions()