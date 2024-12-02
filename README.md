# NLP Text Analysis and Classification Tools

A comprehensive suite of Natural Language Processing (NLP) tools for text analysis and classification. This project includes multiple tools for text analysis, manual classification, and automated classification using spaCy.

## Features

### 1. Text Analysis (1-text_analyzer.py)
- Basic text statistics (word count, sentence count)
- Readability analysis using Gunning Fog Index
- Spell checking with technical term preservation
- Word frequency analysis
- Paragraph-by-paragraph processing
- Automated spelling correction

### 2. Manual Classification (2-manual_classifier.py)
- Manual text classification interface
- Support for custom categories
- Interactive classification process
- Output segregation by category

### 3. SpaCy Classification
- **Manual SpaCy Classifier** (3-manual_spacy_classifier.py)
  - Training data creation
  - Manual labeling interface
  - SpaCy model integration
  
- **Automated SpaCy Classifier** (4-spacy_classifier.py)
  - Automated text classification
  - Pre-trained model utilization
  - Multi-category support

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
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

4. Download required models and data:
```bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
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
