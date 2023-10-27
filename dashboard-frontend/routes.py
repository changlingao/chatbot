#!/usr/bin/env python
# encoding: utf-8

import sys, os
sys.path.append(os.path.abspath('./backend'))
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
app = Flask(__name__)
from dashboard import Dashboard

db = Dashboard()

@app.route('/')
def index():
    usage = db.usage_in_past_30_days()
    response = str(db.get_average_response_time())
    solved = str(db.get_solved_response_percentage())
    rating = list(db.get_rating_count().values())
    convo_time = str(db.get_average_conversation_time())
    usage_weekly = list(db.get_weekly_usage().values())
    usage_dates = list(db.get_weekly_usage().keys())
    pos_fb = db.get_total_positive_feedback()

    return render_template("index.html", pos_fb=pos_fb, usage=usage, response=response, solved=solved, rating=rating, convo_time=convo_time, usage_weekly=usage_weekly, usage_dates=usage_dates)


@app.route('/faq')
def faq():
    all = db.get_all_questions()
    top_keys = list(db.get_top5_most_frequent_question().keys())
    top_q = list(db.get_top5_most_frequent_question().values())
    return render_template("faq.html", all=all, top_keys=top_keys, top_q=top_q)

@app.route('/feedback')
def feedback():
    inaccurate = str(db.get_inaccurate_response_percentage())
    accurate = str(db.get_accurate_response_percentage())
    negative = db.get_all_negative_comments()
    positive = db.get_all_positive_comments()
    pos_fb = db.get_total_positive_feedback()
    neg_fb = db.get_total_negative_feedback()

    return render_template("feedback.html", inaccurate=inaccurate, accurate=accurate, negative=negative, positive=positive, neg_fb=neg_fb, pos_fb=pos_fb)


if __name__ == '__main__':
    app.run()