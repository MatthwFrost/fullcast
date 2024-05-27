import spacy
import re

# Load SpaCy's pre-trained model
nlp = spacy.load("en_core_web_sm")

# Your text
text = """
"Odd, odd, odd," was Lenina's verdict on Bernard Marx. "So odd, indeed, that in the course of the succeeding weeks she had wondered more than once whether she shouldn't change her mind about the New Mexico holiday," she said.
"Alcohol in his blood-surrogate," was Fanny's explanation of every eccentricity. "But Henry, with whom, one evening when they were in bed together," replied Henry.
It was a quiet evening. The sun was setting, casting a golden hue over the horizon.
"""

# Predefined list of character names
characters = ["Lenina", "Bernard", "Fanny", "Henry"]

# Process the text with SpaCy
doc = nlp(text)

# Function to extract dialogue with positions and integrate with attributions
def extract_dialogue_with_attributions(text):
    dialogues = []
    for match in re.finditer(r'"([^"]*)"', text):
        start, end = match.span()
        # Attempt to capture any trailing narrative attributions like "she said"
        post_text = text[end:end+50]
        attribution_match = re.search(r'\s*(, said|, replied)', post_text)
        if attribution_match:
            end_attribution = end + attribution_match.end()
            full_text = text[start:end_attribution]
            dialogues.append((full_text, start, end_attribution))
        else:
            dialogues.append((match.group(0), start, end))
    return dialogues

# Function to associate dialogue and narration
def associate_dialogue_and_narration(text, doc, characters):
    dialogues = extract_dialogue_with_attributions(text)
    last_index = 0
    associations = []
    last_speaker = None

    for dialogue, start, end in dialogues:
        # Check for narration before the dialogue
        if start > last_index:
            narration = text[last_index:start].strip()
            if narration:
                associations.append(("Narrator", narration))
        # Determine speaker by checking the named entities or using the last known speaker
        speaker = None
        containing_sentence = next((sent for sent in doc.sents if sent.start_char <= start and sent.end_char >= end), None)
        if containing_sentence:
            for token in containing_sentence:
                if token.text in characters:
                    speaker = token.text
                    break
            if not speaker and last_speaker:
                speaker = last_speaker

        associations.append((speaker if speaker else "Narrator", dialogue))
        last_speaker = speaker  # Update the last speaker
        last_index = end
    # Check for remaining narration after the last dialogue
    if last_index < len(text):
        remaining_narration = text[last_index:].strip()
        if remaining_narration:
            associations.append(("Narrator", remaining_narration))

    return associations

# Extract and associate dialogues and narration
dialogues_and_narration = associate_dialogue_and_narration(text, doc, characters)

# Print the results
for speaker, content in dialogues_and_narration:
    print(f"{speaker}: {content}")
