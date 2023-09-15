#!/usr/bin/env python
# encoding: utf-8

import model
from flask import Flask, request, render_template, jsonify

import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import sys, os
sys.path.append(os.path.abspath('./backend'))
from main import Mainbot


# This logic would normally be contained elsewhere
# Would probably be placed in the place where flask is
# connect to databse
uri = "mongodb+srv://changlin:chatbot@cluster0.vpvr7e8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# initialize chatbot
chatbot = Mainbot(client.chatbot_database)

app = Flask(__name__)
my_model = model.Model(chatbot)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    message = request.json['message']

    # Implement your chatbot logic here and generate a response
    # pass 'message' over to chatbot and return 'response_message' as chatbot response

    response_message = my_model.get_answer(message)
    return jsonify({"response_message": response_message})


if __name__ == '__main__':

    app.run()
    chatbot.save_to_db()
    client.close()
