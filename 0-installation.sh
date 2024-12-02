#!/bin/bash
#-------------------------------------------------------------#
# brew install python@3.11  # Install Python 3.11 
#-------------------------------------------------------------#
deactivate                  # Exit current venv if active
rm -rf .venv                # Remove the old venv
/usr/local/opt/python@3.11/bin/python3.11 -m venv .venv
#-------------------------------------------------------------#
source .venv/bin/activate
python --version      
#-------------------------------------------------------------#
pip install -U pip setuptools wheel
pip install spacy
python -m spacy download en_core_web_sm
#-------------------------------------------------------------#
source .venv/bin/activate
pip install -r requirements.txt
#-------------------------------------------------------------#
