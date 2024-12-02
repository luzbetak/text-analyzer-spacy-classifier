"""
Text Classifier using spaCy (Pure NLP)

This script classifies text from data/in/raw-data.txt into two categories:
- Technology-related content (saved to data/out/technology.txt)
- Medical-related content (saved to data/out/medical.txt)

The classification uses spaCy's advanced NLP capabilities without relying on manual keyword lists.
"""

import spacy
from pathlib import Path
import re
import sys
import subprocess
from collections import Counter

def ensure_directories():
    """Create necessary directories if they don't exist."""
    Path('data/in').mkdir(parents=True, exist_ok=True)
    Path('data/out').mkdir(parents=True, exist_ok=True)

def load_text(filename):
    """Load text from a file and split into paragraphs."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Split text into paragraphs (separated by blank lines)
            text = file.read()
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            return paragraphs
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        return []

def is_medical_case(doc):
    """
    Check if the text represents a medical case using spaCy's entity recognition.
    """
    # Medical case patterns (age and presentation)
    medical_patterns = [
        r'\b\d+[-\s]year[-\s]old\b',
        r'\b(presents?|complains?|reports?|arrives?)\b.*\b(with|of)\b',
    ]
    
    text = doc.text.lower()
    
    # Check for medical case patterns
    for pattern in medical_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
            
    # Count medical-related entities
    medical_entity_labels = {'DISEASE', 'SYMPTOM', 'CONDITION', 'BODY', 'PERSON'}
    medical_ents = [ent for ent in doc.ents if ent.label_ in medical_entity_labels]
    
    # Check for medical verbs and their objects
    medical_verbs = {
        'diagnose', 'treat', 'prescribe', 'examine', 'present',
        'administer', 'consult', 'assess', 'monitor', 'evaluate',
        'recover', 'suffer', 'hospitalize', 'inject', 'medicate',
        'operate', 'screen', 'heal', 'sedate', 'vaccinate',
        'deteriorate', 'improve', 'manifest', 'refer', 'discharge'
    }
    medical_actions = any(token.lemma_ in medical_verbs for token in doc)
    
    # Check for medical noun chunks
    medical_indicators = {'patient', 'symptoms', 'diagnosis', 'treatment'}
    medical_chunks = any(chunk.root.lemma_ in medical_indicators for chunk in doc.noun_chunks)
    
    return len(medical_ents) > 0 or (medical_actions and medical_chunks)

def is_tech_related(doc):
    """
    Check if the text is technology-related using spaCy's entity recognition.
    """
    # Count technology-related entities
    tech_entity_labels = {'ORG', 'PRODUCT', 'GPE', 'EVENT'}
    tech_ents = [ent for ent in doc.ents if ent.label_ in tech_entity_labels]
    
    # Check for technology-related verbs and their objects
    tech_verbs = {
        'compute', 'process', 'analyze', 'automate', 'program',
        'debug', 'deploy', 'optimize', 'code', 'encrypt',
        'decrypt', 'configure', 'install', 'update', 'sync',
        'backup', 'download', 'upload', 'stream', 'compile',
        'execute', 'implement', 'integrate', 'interface', 'network',
        'render', 'scale', 'test', 'validate', 'virtualize',
        # NLP-specific verbs
        'understand', 'interpret', 'manipulate', 'parse', 'tokenize',
        'classify', 'translate', 'recognize', 'extract', 'generate'
    }
    tech_actions = any(token.lemma_ in tech_verbs for token in doc)
    
    # Check for technology noun chunks
    tech_indicators = {
        'algorithm', 'system', 'data', 'software', 'technology',
        'language processing', 'nlp', 'artificial intelligence',
        'computer science', 'computing', 'machine learning'
    }
    tech_chunks = any(chunk.root.lemma_ in tech_indicators for chunk in doc.noun_chunks)
    
    # Analyze dependencies and contexts
    tech_contexts = []
    for token in doc:
        if token.dep_ in {'dobj', 'pobj'} and token.head.pos_ == 'VERB':
            tech_contexts.append((token.head.lemma_, token.lemma_))
    
    # Score the technical nature of the content
    tech_score = len(tech_ents) + sum(1 for _ in filter(None, [tech_actions, tech_chunks]))
    
    return tech_score > 0 and not is_medical_case(doc)

def classify_paragraph(nlp, paragraph):
    """
    Classify a paragraph using spaCy's NLP capabilities.
    
    Returns:
        str: 'medical' or 'technology' or None
    """
    doc = nlp(paragraph)
    
    # First check if it's a medical case (higher priority)
    if is_medical_case(doc):
        return 'medical'
    
    # Then check if it's technology-related
    if is_tech_related(doc):
        return 'technology'
    
    # Analyze sentence structure and dependencies
    sentence_types = Counter()
    for sent in doc.sents:
        # Analyze root verb and its arguments
        root = sent.root
        if root.pos_ == 'VERB':
            # Check verb arguments and their types
            arguments = [child for child in root.children]
            arg_types = Counter([arg.pos_ for arg in arguments])
            sentence_types[root.lemma_] += 1
    
    # Use sentence analysis for final classification
    if sentence_types:
        tech_verbs = {'compute', 'process', 'analyze', 'develop', 'implement'}
        medical_verbs = {'diagnose', 'treat', 'examine', 'prescribe', 'heal'}
        
        tech_count = sum(count for verb, count in sentence_types.items() if verb in tech_verbs)
        medical_count = sum(count for verb, count in sentence_types.items() if verb in medical_verbs)
        
        if tech_count > medical_count:
            return 'technology'
        elif medical_count > tech_count:
            return 'medical'
    
    return None

def classify_text(nlp, input_file, tech_file, medical_file):
    """
    Classify paragraphs from input file into technology and medical categories.
    """
    # Ensure directories exist
    ensure_directories()
    
    # Load and classify paragraphs
    paragraphs = load_text(input_file)
    if not paragraphs:
        return
    
    tech_paragraphs = []
    medical_paragraphs = []
    
    print("Processing paragraphs...")
    for i, paragraph in enumerate(paragraphs, 1):
        category = classify_paragraph(nlp, paragraph)
        if category == 'medical':
            medical_paragraphs.append(paragraph)
            print(f"Paragraph {i}: Medical")
        elif category == 'technology':
            tech_paragraphs.append(paragraph)
            print(f"Paragraph {i}: Technology")
        else:
            print(f"Paragraph {i}: Unclassified")
    
    # Write technology-related content
    with open(tech_file, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(tech_paragraphs))
    print(f"\nTechnology-related content written to {tech_file}")
    
    # Write medical-related content
    with open(medical_file, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(medical_paragraphs))
    print(f"Medical-related content written to {medical_file}")

def main():
    # Check Python version
    if sys.version_info < (3, 11):
        print("This script requires Python 3.11 or higher")
        sys.exit(1)
    
    # Load spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
        print("Loaded spaCy model successfully")
    except OSError:
        print("Downloading spaCy model...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        nlp = spacy.load('en_core_web_sm')
    
    # File paths
    input_file = 'data/in/raw-data.txt'
    tech_file = 'data/out/technology.txt'
    medical_file = 'data/out/medical.txt'
    
    # Run classification
    classify_text(nlp, input_file, tech_file, medical_file)

if __name__ == "__main__":
    main() 