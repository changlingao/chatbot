import sys, os
sys.path.append(os.path.abspath('./backend'))
import main

class Model:

    def __init__(self, chatbot):
        self.answer = "hello"
        self.chatbot = chatbot

    def set_answer(self, new_answer):
        self.answer = new_answer
    
    def get_answer(self, question):
        self.answer = main.answer(question, self.chatbot)
        return self.answer
    