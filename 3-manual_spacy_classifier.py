"""
Text Classifier using spaCy

This script classifies text from data/in/raw-data.txt into two categories:
- Technology-related content (saved to data/out/technology.txt)
- Medical-related content (saved to data/out/medical.txt)

The classification uses spaCy's NLP capabilities for more accurate text classification.
"""

import spacy
from pathlib import Path
import re
import sys
import subprocess

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
    # Check for medical case patterns
    medical_patterns = [
        r'\b\d+[-\s]year[-\s]old\b',
        r'\b(presents?|complains?|reports?|arrives?)\b.*\b(with|of)\b',
    ]
    
    text = doc.text.lower()
    
    # Check for medical case patterns
    for pattern in medical_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    # Check for medical entities and common medical terms
    medical_ents = [ent for ent in doc.ents if ent.label_ in {'DISEASE', 'SYMPTOM'}]
    medical_terms = {'pain', 'symptoms', 'diagnosis', 'treatment', 'patient'}
    
    if medical_ents or any(term in text for term in medical_terms):
        return True
    
    return False

def classify_paragraph(nlp, paragraph):
    """
    Classify a paragraph using spaCy's NLP capabilities.
    
    Returns:
        str: 'medical' or 'technology' or None
    """
    doc = nlp(paragraph)
    
    # First check if it's a medical case
    if is_medical_case(doc):
        return 'medical'
    
    # Technology-related terms and patterns
    tech_terms = {
        'technology', 'computer', 'artificial intelligence', 'ai', 'machine learning',
        'nlp', 'algorithm', 'digital', 'chatbot', 'analytics', 'data science',
        'neural network', 'deep learning', 'automation', 'programming'
    }
    
    # Medical-related terms
    medical_terms = {
        'patient', 'diagnosis', 'symptoms', 'treatment', 'disease', 'hospital',
        'doctor', 'clinical', 'medical', 'surgery', 'medication', 'therapy',
        'healthcare', 'physician', 'nurse', 'clinic'
    }
    
    # Convert paragraph to lowercase for term matching
    text_lower = paragraph.lower()
    
    # Count matches for each category
    tech_count = sum(1 for term in tech_terms if term in text_lower)
    medical_count = sum(1 for term in medical_terms if term in text_lower)
    
    # Check for technology-specific entities
    tech_ents = [ent for ent in doc.ents if ent.label_ in {'ORG', 'PRODUCT', 'GPE'} 
                 and any(term in ent.text.lower() for term in tech_terms)]
    tech_count += len(tech_ents)
    
    # Classify based on the stronger match
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