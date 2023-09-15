
import pytest

from .similarity_algo import *
import os
import sys

sys.path.append('../backend')  # Add the parent directory to the Python path
from main import Mainbot

@pytest.fixture
def sut():
	bot = Mainbot()
	return bot

#testing to ask MAX X Build tray options
def test_MAX_x_build(sut):
	
	result = sut.ask_chatbot(["hey there","What are MAX X Build tray options","exit"])
	
	file_contents = None

	file_name = 'maintaining-the-build-tray-max-x-1.txt'

	file_path =create_absolute_path(file_name)

	try:
	    # Your code that may raise a FileNotFoundError
		with open(file_path, 'r') as file:
			file_contents = ''.join(file.readlines()[1:])
			
	except FileNotFoundError as e:
		print("File not found. Full path:", e.filename)

	chatbot_response = result[1]

	accuracy = count_accuracy(file_contents,chatbot_response)
	
	assert accuracy>60



def test_calibrate_pro4k(sut):
	
	result = sut.ask_chatbot(["hiiii","How to calibrate the PRO 4K platform","exit"])
	
	file_contents = None

	file_name = 'maintenance-schedule-pro-4k-3.txt'

	file_path =create_absolute_path(file_name)

	try:
	    # Your code that may raise a FileNotFoundError
		with open(file_path, 'r') as file:
			file_contents = ''.join(file.readlines()[1:])
			
	except FileNotFoundError as e:
		print("File not found. Full path:", e.filename)

	chatbot_response = result[1]

	accuracy = count_accuracy(file_contents,chatbot_response)
	
	assert accuracy>60

#test_calibrate_pro4k(sut())

