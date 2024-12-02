# Text Readability Analyzer

A Python-based tool for analyzing text readability, complexity, and quality. It provides comprehensive metrics including Gunning Fog Index, spell checking, and detailed text statistics.

## Features

- **Text Analysis**
  - Word count and unique words
  - Sentence count
  - Average words per sentence
  - Most common words (excluding stop words)
  - Word frequency distribution

- **Readability Analysis**
  - Gunning Fog Index calculation
  - Complex word identification
  - Syllable counting
  - Education level estimation

- **Spell Checking**
  - Automatic spell correction
  - Technical term preservation (NLP, AI, etc.)
  - Proper handling of contractions
  - Detailed correction reporting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/luzbetak/text-readability-analyzer.git
cd text-readability-analyzer
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your text in a file (e.g., `data/raw-data.txt`)

2. Run the analyzer:
```bash
python text_analyzer.py
```

The tool will:
- Analyze each paragraph separately
- Show original and corrected text (if spell checking is needed)
- Display detailed statistics and readability metrics
- Save corrected text to `data/fix-data.txt`

## Output Metrics

### Basic Statistics
- Number of sentences
- Number of words
- Number of unique words
- Average words per sentence
- Most common words

### Readability Analysis (Gunning Fog Index)
- Overall readability score
- Required education level
- Average sentence length
- Percentage of complex words
- Number of complex words

### Spell Check Results
- Original text
- Corrected text
- List of corrections made
- Summary of all corrections

## Requirements

- Python 3.6+
- NLTK 3.8.1
- pyspellchecker 0.8.1

## Project Structure

```
.
├── README.md
├── requirements.txt
├── text_analyzer.py
├── text_classifier.py
└── data/
    ├── in/
    │   └── raw-data.txt
    └── out/
        ├── technology.txt
        ├── medical.txt
        └── corrected-spelling-data.txt
```

The project structure is organized as follows:
- `text_analyzer.py`: Main script for text analysis and spell checking
- `text_classifier.py`: Script for classifying text into technology and medical categories
- `data/in/`: Directory for input files
  - `raw-data.txt`: Original text file to be processed
- `data/out/`: Directory for output files
  - `technology.txt`: Technology-related content
  - `medical.txt`: Medical-related content
  - `corrected-spelling-data.txt`: Spell-checked and corrected text

## How It Works

### Text Processing
1. Text is split into paragraphs
2. Each paragraph is analyzed separately
3. Spell checking is performed
4. Readability metrics are calculated

### Gunning Fog Index
The Gunning Fog Index estimates the years of formal education needed to understand the text on first reading. Formula:
```
0.4 * (average_sentence_length + percentage_of_complex_words)
```
where complex words are those with three or more syllables.
