"""
Text Classifier

This script classifies text from data/in/raw-data.txt into two categories:
- Technology-related content (saved to data/out/technology.txt)
- Medical-related content (saved to data/out/medical.txt)

The classification is based on keyword matching and paragraph analysis.
"""

import re
from pathlib import Path

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

def is_technology_related(paragraph):
    """
    Determine if a paragraph is technology-related based on keywords and context.
    """
    tech_keywords = {
        'technology', 'computer', 'artificial intelligence', 'ai', 'machine learning',
        'nlp', 'algorithm', 'digital', 'chatbot', 'analytics', 'data',
        'recommendation', 'facial recognition', 'autonomous', 'smart'
    }
    
    # Convert paragraph to lowercase for case-insensitive matching
    paragraph_lower = paragraph.lower()
    
    # First check if it's a medical case - if so, it's not technology-related
    if is_medical_case(paragraph_lower):
        return False
    
    # Count how many tech keywords are present
    keyword_count = sum(1 for keyword in tech_keywords 
                       if keyword in paragraph_lower)
    
    return keyword_count > 0

def is_medical_case(text):
    """
    Check if the text represents a medical case presentation.
    """
    # Common patterns in medical cases
    patterns = [
        r'\b\d+[-\s]year[-\s]old\b',  # Age pattern
        r'\b(presents?|complains?|reports?|arrives?)\b.*\b(with|of)\b',  # Presentation pattern
        r'\bpatient\b',  # Patient reference
        r'\bdiagnosis\b',  # Diagnosis mention
        r'\b(symptoms?|signs?)\b',  # Symptoms/signs
        r'\b(pain|ache|discomfort)\b',  # Pain/discomfort
        r'\b(treatment|medication)\b',  # Treatment-related
        r'\b(medical|clinical)\b',  # Medical context
        r'\b(doctor|physician|nurse)\b',  # Healthcare providers
        r'\b(hospital|clinic|emergency)\b',  # Healthcare settings
    ]
    
    # Check for medical case patterns
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False

def is_medical_related(paragraph):
    """
    Determine if a paragraph is medical-related based on keywords, patterns, and context.
    """
    medical_keywords = {
        'patient', 'diagnosis', 'symptoms', 'pain', 'medical', 'clinical',
        'treatment', 'disease', 'hospital', 'doctor', 'fever', 'bleeding',
        'presents with', 'complains of', 'injury', 'swelling', 'fatigue',
        'nausea', 'vomiting', 'headache', 'chest', 'heart', 'breathing',
        'blood', 'medication', 'surgery', 'examination', 'condition',
        'chronic', 'acute', 'prescription', 'therapy', 'healthcare'
    }
    
    # Convert paragraph to lowercase for case-insensitive matching
    paragraph_lower = paragraph.lower()
    
    # First check if it's a medical case
    if is_medical_case(paragraph_lower):
        return True
    
    # Count how many medical keywords are present
    keyword_count = sum(1 for keyword in medical_keywords 
                       if keyword in paragraph_lower)
    
    return keyword_count > 0

def classify_text(input_file, tech_file, medical_file):
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
    
    for paragraph in paragraphs:
        # Check medical first, as it's more specific
        if is_medical_related(paragraph):
            medical_paragraphs.append(paragraph)
        elif is_technology_related(paragraph):
            tech_paragraphs.append(paragraph)
    
    # Write technology-related content
    with open(tech_file, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(tech_paragraphs))
    print(f"Technology-related content written to {tech_file}")
    
    # Write medical-related content
    with open(medical_file, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(medical_paragraphs))
    print(f"Medical-related content written to {medical_file}")

def main():
    # File paths with new directory structure
    input_file = 'data/in/raw-data.txt'
    tech_file = 'data/out/technology.txt'
    medical_file = 'data/out/medical.txt'
    
    # Run classification
    classify_text(input_file, tech_file, medical_file)

if __name__ == "__main__":
    main() 