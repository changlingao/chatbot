#!/bin/bash
pip install virtualenv
python -m venv venv
source venv/Scripts/activate
python -m pip install -r requirements.txt
cd backend
python main.py
pip install langchain