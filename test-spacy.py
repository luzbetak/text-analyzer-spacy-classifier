import spacy

# Load the English model
nlp = spacy.load('en_core_web_sm')

# Test with a simple sentence
doc = nlp("This is a test sentence.")
print("SpaCy is working!")

# Print tokens to verify processing
for token in doc:
    print(token.text)
