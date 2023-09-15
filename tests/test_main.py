import pytest
from backend import main

@pytest.fixture
def sut():
	bot = main.Mainbot(None)
	return bot

@pytest.fixture
def sut2():
	#with db
	bot = main.Mainbot(None)
	return bot

def test_askchatbot(sut):
	actual = sut.ask_chatbot("what is a question?")
	expected = True
	assert len(actual) > 0

# def test_askchatbot_savesmessage(sut):
# 	question = "what is delamination"
# 	answer = sut.ask_chatbot(question)
# 	history = sut.get_chat_history()

# 	chquestion = history['question']
# 	chanswer = history['answer']
# 	assert question == chquestion
# 	assert answer == chanswer
# 	assert len(history['qtime']) > 0
# 	assert len(history['atime']) > 0
# 	assert len(history['source']) > 0


def test_askchatbot_none(sut):
	actual = sut.ask_chatbot("")
	expected = ""
	assert actual == expected

# def test_savetodb_empty(sut):
# 	actual = sut.save_to_db()
# 	expected = False
# 	assert actual == expected 
	
# def test_savemessage_none(sut):
# 	actual = sut.save_message("", "qtime", "answer", "atime", "src")

# 	history = sut.get_chat_history()
# 	assert len(history) == 0
# 	expected = False
# 	assert actual == expected
	
# 	actual = sut.save_message("question", "", "answer", "atime", "src")
# 	history = sut.get_chat_history()
# 	assert len(history) == 0
# 	assert actual == expected

# def test_savemessage(sut):
# 	actual = sut.save_message("question", "qtime", "answer", "atime", "src")
# 	expected = True
# 	assert actual == expected

# 	history = sut.get_chat_history()
# 	assert len(history) == 1
# 	assert history['question'] == "question"
# 	assert history['qtime'] == "qtime"
# 	assert history['answer'] == "answer"
# 	assert history['atime'] == "atime"
# 	assert history['source'] == "src"

def test_savetodb_nodb(sut):
	actual = sut.save_to_db()
	expected = False

	assert actual == expected

def test_savetodb(sut2):
	#db connect with sut2

	assert True
    



	
	



