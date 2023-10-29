#!/usr/bin/env python
# encoding: utf-8

import sys, os
sys.path.append(os.path.abspath('./backend'))
from flask import Flask, request, render_template, jsonify, session
import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from main import Mainbot

import uuid
import secrets


# Connect to database
uri = "mongodb+srv://changlin:chatbot@cluster0.vpvr7e8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Initialize chatbot
chatbot = Mainbot(client.chatbot_database)
app = Flask(__name__)

# Flask built in session management
app.secret_key = secrets.token_hex(16)  # Generate a random secret key


@app.route('/')
def index():
    # Session management
    if 'session_id' not in session:
        # Generate a unique session ID
        # uuid1: zero chance of collisions since it uses current time
        session['session_id'] = str(uuid.uuid1())

    return render_template("index.html")


@app.route('/expand')
def expand():
    # Render expanded chatbot page
    return render_template("expand.html")


@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    # Input user query to chatbot and return its response message
    message = request.json['message']
    session_id = session['session_id']
    response_message = chatbot.ask_chatbot(session_id=session_id, provided_question=message)
    return jsonify({"response_message": response_message})


@app.route('/chat_history', methods=['GET'])
def get_history():
    # If user previously used chatbot without closing, retrieve chat history
    chat_log_output = []
    try:
        chat_log = chatbot.get_chat_history_by_session(session_id=session['session_id'])
    except KeyError:
        return jsonify({"history": chat_log_output})
        
    # Embed html tags for images, gifs, videos and links for each retrieved chatbot message
    for i in range(len(chat_log)):
        chat_log_output.append(chat_log[i].copy())
        chat_log_output[i]["answer"] = chatbot.embedding_format(chat_log[i]["answer"])
    return jsonify({"history": chat_log_output})


@app.route('/feedback', methods=['POST'])
def receive_feedback():
    # Collect user-provided feedback
    feedbackType = request.form.get("feedbackType")
    comment = request.form.get("comment")
    rating = request.form.get("rating")
    checklist = request.form.getlist("feedback")
    feedback_ls = [feedbackType, comment, rating, checklist]

    # Save feedback to database according to user's session id
    chatbot.save_feedback(session_id=session["session_id"], feedback_ls=feedback_ls)
    return ("", 204)


@app.route('/close', methods=['GET'])
def close_chat():
    session_id = session['session_id']
    # Save user chat log and feedback to database
    chatbot.save_to_db(session_id)

    # Clear the session for this user
    session.pop('session_id', None)

    return jsonify({"message": "Chat terminated"})


if __name__ == '__main__':
    app.run()
    client.close()
