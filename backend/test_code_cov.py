
#To run code coverage test, from backend folder run 'python3.11 -m coverage run -m pytest'
#Then to generate html report, run 'python3.11 -m coverage html'


import pytest

from main import Mainbot

@pytest.fixture
def sut():
	bot = Mainbot()
	return bot

#testing to ask MAX X Build tray options
def test_printer_options(sut):
	
	result = sut.ask_chatbot(["hey there","What are different printer options","exit"])

def test_no_exit(sut):
	
	result = sut.ask_chatbot(["hey there","clean basin","electrocution error"])
	
	


