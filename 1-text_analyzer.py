"""
Text Analyzer

This module provides comprehensive text analysis functionality including:
- Basic text statistics (word count, sentence count, etc.)
- Readability analysis using Gunning Fog Index
- Spell checking with technical term preservation
- Word frequency analysis

The tool is designed to process text paragraph by paragraph, providing detailed
metrics for each section as well as overall text analysis.
"""

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import Counter
import string
from spellchecker import SpellChecker
from pathlib import Path

def count_complex_words(words):
    """
    Count words with three or more syllables.
    
    Args:
        words (list): List of words to analyze
        
    Returns:
        int: Number of complex words (words with 3+ syllables)
        
    Note:
        Words ending in -es, -ed, or -ing are not counted as complex
        to avoid overestimating text complexity.
    """
    complex_words = 0
    for word in words:
        syllable_count = count_syllables(word)
        if syllable_count >= 3:
            # Exclude common suffixes like -es, -ed, or -ing
            if not (word.endswith(('es', 'ed', 'ing'))):
                complex_words += 1
    return complex_words

def count_syllables(word):
    """
    Count the number of syllables in a word using vowel group counting.
    
    Args:
        word (str): Word to count syllables in
        
    Returns:
        int: Number of syllables
        
    Note:
        Uses a simple vowel counting algorithm with adjustments for:
        - Silent 'e' at word end
        - Consecutive vowels counted as one
        - Minimum syllable count of 1
    """
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    
    # Count first vowel
    if word[0] in vowels:
        count += 1
        
    # Count vowel groups
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    
    # Adjust for silent 'e'
    if word.endswith('e'):
        count -= 1
    
    # Ensure minimum of 1 syllable
    return max(1, count)

def calculate_gunning_fog(text):
    """
    Calculate the Gunning Fog Index for text readability.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Dictionary containing:
            - gunning_fog_index: The calculated index
            - avg_sentence_length: Average words per sentence
            - percent_complex_words: Percentage of complex words
            - complex_word_count: Number of complex words
            
    Note:
        The Gunning Fog Index estimates years of formal education
        needed to understand the text on first reading.
    """
    sentences = sent_tokenize(text)
    words = [word.lower() for word in word_tokenize(text) 
            if word not in string.punctuation]
    
    avg_sentence_length = len(words) / len(sentences)
    complex_word_count = count_complex_words(words)
    percent_complex_words = (complex_word_count / len(words)) * 100
    gunning_fog = 0.4 * (avg_sentence_length + percent_complex_words)
    
    return {
        'gunning_fog_index': gunning_fog,
        'avg_sentence_length': avg_sentence_length,
        'percent_complex_words': percent_complex_words,
        'complex_word_count': complex_word_count
    }

def fix_spelling(text):
    """
    Fix spelling errors while preserving technical terms.
    
    Args:
        text (str): Text to check for spelling errors
        
    Returns:
        tuple: (corrected_text, list_of_corrections)
            - corrected_text: Text with spelling fixes
            - list_of_corrections: List of (original, corrected) pairs
            
    Note:
        Preserves technical terms, abbreviations, and contractions.
        Maintains original spacing and punctuation.
    """
    spell = SpellChecker()
    
    # Add technical terms to the dictionary
    technical_terms = {
        'NLP', 'AI', 'pangram', 'chatbots', 'analytics',
        'algorithm', 'algorithms', 'analytics'
    }
    for term in technical_terms:
        spell.word_frequency.load_words([term])
    
    words = word_tokenize(text)
    corrections = []
    fixed_words = []
    
    for word in words:
        # Skip punctuation, numbers, and known terms
        if (word in string.punctuation or word.isdigit() or 
            word in technical_terms or word.isupper()):
            fixed_words.append(word)
            continue
            
        # Preserve contractions
        if "'" in word:
            fixed_words.append(word)
            continue
            
        # Check spelling
        if not spell.known([word.lower()]):
            correction = spell.correction(word)
            if correction and correction != word:
                corrections.append((word, correction))
                fixed_words.append(correction)
            else:
                fixed_words.append(word)
        else:
            fixed_words.append(word)
    
    # Reconstruct text with proper spacing
    fixed_text = ""
    for i, word in enumerate(fixed_words):
        if i > 0 and not word in string.punctuation:
            fixed_text += " "
        fixed_text += word
    
    return fixed_text, corrections

def analyze_text(text):
    """
    Perform comprehensive text analysis.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Dictionary containing various text metrics:
            - Basic statistics (word count, sentence count, etc.)
            - Word frequency information
            - Readability metrics
            
    Note:
        Downloads required NLTK data if not already present.
    """
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

    # Basic statistics
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word not in string.punctuation]
    
    # Remove stopwords for frequency analysis
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Calculate metrics
    freq_dist = FreqDist(filtered_words)
    readability = calculate_gunning_fog(text)
    
    return {
        'num_sentences': len(sentences),
        'num_words': len(words),
        'num_unique_words': len(set(words)),
        'avg_words_per_sentence': len(words) / len(sentences) if len(sentences) > 0 else 0,
        'most_common_words': dict(freq_dist.most_common(5)),
        'word_frequency': dict(Counter(filtered_words)),
        'readability': readability
    }

def print_analysis(results, paragraph_num):
    """
    Print text analysis results in a readable format.
    
    Args:
        results (dict): Analysis results from analyze_text()
        paragraph_num (int): Paragraph number for identification
        
    Note:
        Outputs:
        - Basic text statistics
        - Readability metrics
        - Most common words
    """
    print(f"\n=== Paragraph {paragraph_num} Analysis ===")
    print(f"Number of sentences: {results['num_sentences']}")
    print(f"Number of words: {results['num_words']}")
    print(f"Number of unique words: {results['num_unique_words']}")
    print(f"Average words per sentence: {results['avg_words_per_sentence']:.2f}")
    
    readability = results['readability']
    print("\nReadability Analysis:")
    print(f"Gunning Fog Index: {readability['gunning_fog_index']:.1f}")
    print(f"  - This text requires approximately {int(round(readability['gunning_fog_index']))} years of formal education to understand")
    print(f"  - Average sentence length: {readability['avg_sentence_length']:.1f} words")
    print(f"  - Percentage of complex words: {readability['percent_complex_words']:.1f}%")
    print(f"  - Number of complex words: {readability['complex_word_count']}")
    
    print("\nMost common words:")
    for word, count in results['most_common_words'].items():
        print(f"  {word}: {count}")

def ensure_directories():
    """Create necessary directories if they don't exist."""
    Path('data/in').mkdir(parents=True, exist_ok=True)
    Path('data/out').mkdir(parents=True, exist_ok=True)

def process_text_file(input_file, output_file=None):
    """
    Process a text file paragraph by paragraph with full analysis.
    
    Args:
        input_file (str): Path to input text file
        output_file (str, optional): Path to save corrected text
        
    Note:
        - Processes text paragraph by paragraph
        - Performs spell checking and text analysis
        - Saves corrected text if output_file is specified
        - Prints detailed analysis for each paragraph
    """
    # Ensure directories exist
    ensure_directories()
    
    try:
        with open(input_file, 'r') as file:
            text = file.read()
            
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        print(f"\nFound {len(paragraphs)} paragraphs in the text file.")
        
        fixed_paragraphs = []
        all_corrections = []
        
        for i, paragraph in enumerate(paragraphs, 1):
            print(f"\n--- Paragraph {i} ---")
            print("Original:", paragraph)
            
            fixed_text, corrections = fix_spelling(paragraph)
            fixed_paragraphs.append(fixed_text)
            print("Corrected:", fixed_text)
            
            if corrections:
                print("\nSpelling corrections:")
                for original, corrected in corrections:
                    print(f"  {original} -> {corrected}")
                all_corrections.extend(corrections)
            
            results = analyze_text(fixed_text)
            print_analysis(results, i)
        
        if output_file:
            with open(output_file, 'w') as file:
                file.write('\n\n'.join(fixed_paragraphs))
            print(f"\nCorrected text saved to {output_file}")
            
        if all_corrections:
            print("\n=== Summary of All Corrections ===")
            for original, corrected in all_corrections:
                print(f"{original} -> {corrected}")
            
    except FileNotFoundError:
        print(f"Error: Could not find file {input_file}")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    # Process the text file and save corrections
    process_text_file('data/in/raw-data.txt', 'data/out/corrected-spelling-data.txt') 