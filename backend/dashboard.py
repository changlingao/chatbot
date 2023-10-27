#!/usr/bin/env python
# encoding: utf-8

import sys, os
sys.path.append(os.path.abspath('./backend'))
import certifi
import uuid
import copy
import secrets

from main import Mainbot
from flask import Flask, request, render_template, jsonify, session
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from collections import Counter
from datetime import timedelta
URI = "mongodb+srv://changlin:chatbot@cluster0.vpvr7e8.mongodb.net/?retryWrites=true&w=majority"



class Dashboard:
    def __init__(self):
        self.client = None
        try:
            self.client = MongoClient(URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            db = self.client['chatbot_database']
            collection = db['chats']
            self.result = list(collection.find())
        except Exception as e:
            return e

    def get_total_positive_feedback(self) -> int:
        if self.client is None:
            return 0

        positive_count = 0
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='positive':
                        positive_count+=1
        return positive_count


    def get_total_negative_feedback(self) -> int:
        if self.client is None:
            return 0

        negative_count = 0 
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='negative':
                        negative_count+=1
        return negative_count

    def get_percentage_of_positive_feedback(self) -> float:
        total_feedback_count = 0 
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    total_feedback_count+=1

        return(round(self.get_total_positive_feedback()/total_feedback_count*100,2))

    def get_all_positive_comments(self) -> list:

        comment_list = []
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='positive' and chats['feedback'][1]!='':

                        comment_list.append(chats['feedback'][1])

        return comment_list

    def get_all_negative_comments(self) -> list:

        comment_list = []
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='negative' and chats['feedback'][1]!='':
                        comment_list.append(chats['feedback'][1])

        return comment_list



    def get_rating_count(self) -> dict:

        rating_count = {}
        rating_count['1 star'] = 0
        rating_count['2 star'] = 0
        rating_count['3 star'] = 0
        rating_count['4 star'] = 0
        rating_count['5 star'] = 0

        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][2] is not None:
                        #ADDED 'STARS' TO THE DICTIONARY TO SIMPLIFY READING, replace with the other star_key variable to remove 'stars' from the dictionary
                        star_key = str(chats['feedback'][2])+" star"
                        #star_key = chats['feedback'][2]

                        if star_key not in rating_count:
                            rating_count[star_key] = 1
                        else:
                            rating_count[star_key]+=1

        return rating_count

        
    #function to return the percentage of users ticking the solved checkbox in respect to giving positive feedback
    def get_solved_response_percentage(self) -> float:

        solved_count = 0
        positive_count = 0
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='positive':
                        positive_count+=1
                        if 'solved' in chats['feedback'][3]:
                            solved_count+=1
        
        return round((solved_count/positive_count*100),2)

    #function to return the percentage of users ticking the unsolved checkbox in respect to giving negative feedback
    def get_unsolved_response_percentage(self) -> float:

        unsolved_count = 0
        negative_count = 0
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='negative':
                        negative_count+=1
                        if 'unsolved' in chats['feedback'][3]:
                            unsolved_count+=1

        return round((unsolved_count/negative_count*100),2)

    #function to return the percentage of users ticking the accurate checkbox in respect to giving positive feedback
    def get_accurate_response_percentage(self) -> float:

        accurate_count = 0
        positive_count = 0
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='positive':
                        positive_count+=1
                        if 'accurate' in chats['feedback'][3]:
                            accurate_count+=1

        return round((accurate_count/positive_count*100),2)

    #function to return the percentage of users ticking the innacurate checkbox in respect to giving negative feedback
    def get_inaccurate_response_percentage(self) -> float:

        inaccurate_count = 0
        negative_count = 0
        for session in self.result:
            for chats in session['chat_history']:
                if 'feedback' in chats:
                    if chats['feedback'][0]=='negative':
                        negative_count+=1
                        if 'inaccurate' in chats['feedback'][3]:
                            inaccurate_count+=1

        return round((inaccurate_count/negative_count*100),2)


    #for the past 30 days, in seconds
    def get_average_conversation_time(self) -> float:

        if self.client is None:
            return 0
        
        total_questions = 0
        total_conversation_time = 0
        current_datetime = datetime.now()

        for session in self.result:

            

            start_convo = session['chat_history'][0]['qtime']
            end_convo = session['chat_history'][-1]['atime']

            if ((current_datetime-start_convo).total_seconds()>25992000):
                continue
            
            total_conversation_time+=(end_convo - start_convo).total_seconds()
            total_questions+=1

        return round((total_conversation_time/total_questions),2)





    def usage_in_past_30_days(self) -> int:
        if self.client is None:
            return 0
        
        total_usage = 0
        current_datetime = datetime.now()

        for session in self.result:
            start_datetime =session['chat_history'][0]['qtime']

            if ((current_datetime-start_datetime).total_seconds()>25992000):
                continue
            else:
                total_usage += 1
        return total_usage

    #for the past 30 days
    def get_average_response_time(self) -> float:
        if self.client is None:
            return 0
        
        total_questions = 0
        total_response_time = 0
        current_datetime = datetime.now()

        for session in self.result:

            start_datetime =session['chat_history'][0]['qtime']

            if ((current_datetime-start_datetime).total_seconds()>25992000):
                continue

            for chats in session['chat_history']:
                time_diff = (chats['atime'] - chats['qtime']).total_seconds()
                total_questions += 1
                total_response_time += time_diff

        average_resp_time = total_response_time/total_questions
        return round(average_resp_time,2)

    #get all questions
    def get_all_questions(self) -> list:
        list_of_chats=[]
        for session in self.result:
            for chats in session['chat_history']:
                list_of_chats.append(chats['question'])

        return list_of_chats



    #weekly usage for the past 4 weeks
    def get_weekly_usage(self) -> dict:

        if self.client is None:
            return 0
        
        usage_dict = {}
        current_datetime = datetime.now()
        one = current_datetime-timedelta(weeks=1)
        two = current_datetime-timedelta(weeks=2)
        three = current_datetime-timedelta(weeks=3)
        four = current_datetime-timedelta(weeks=4)

        usage_dict[one.strftime("%Y-%m-%d")]=0
        usage_dict[two.strftime("%Y-%m-%d")]=0
        usage_dict[three.strftime("%Y-%m-%d")]=0
        usage_dict[four.strftime("%Y-%m-%d")]=0


        for session in self.result:
            start_datetime =session['chat_history'][0]['qtime']
            one_week = 604800
            usage_date = (current_datetime-start_datetime).total_seconds()



            if (usage_date>0 and usage_date<one_week):
                usage_dict[one.strftime("%Y-%m-%d")]+= 1
            #usage in the period of last two weeks
            elif (usage_date>one_week and usage_date<(one_week*2)):
                usage_dict[two.strftime("%Y-%m-%d")]+= 1
            #usage in the period of last three weeks
            elif (usage_date>(one_week*2) and usage_date<(one_week*3)):
                usage_dict[three.strftime("%Y-%m-%d")]+= 1
            #usage in the period of last four weeks
            elif (usage_date>(one_week*3) and usage_date<(one_week*4)):
                usage_dict[four.strftime("%Y-%m-%d")]+= 1

        return usage_dict

        



    #get most frequent questions
    def get_top5_most_frequent_question(self)-> dict:

        if self.client is None:
            return 0


        common_words= ['is','to','where','what','how','a','the','hi','my','do','i']
        list_of_chats = []
        for session in self.result:
            for chats in session['chat_history']:
                list_of_chats.append(chats['question'])

        #print(list_of_chats)
        
        word_frequency_map = {}

        # Process each string in the list
        for index, string in enumerate(list_of_chats):

            word_counts  = Counter(string.split())


            for word, count in word_counts.items():
                if word not in common_words:
                    if word in word_frequency_map:
                        word_frequency_map[word].append((index, count))
                    else:
                        word_frequency_map[word] = [(index, count)]

        # Sort the dictionary by the sum of word frequencies in descending order
        sorted_word_frequency = sorted(word_frequency_map.items(), key=lambda x: sum(count for _, count in x[1]), reverse=True)

        # Output the top 5 words and their corresponding strings
        top_5_words = sorted_word_frequency[:5]
        '''
        for word, indices in top_5_words:
            print(f"Word: '{word}', Total Frequency: {sum(count for _, count in indices)}")
            for index, count in indices:
                print(f" - String at index {index}: '{list_of_chats[index]}' (Word Count: {count})")
        '''

        frequent_question_dict = {}

        for word, indices in top_5_words:
            frequent_question_dict[word]= []
            
            for index, count in indices:
                frequent_question_dict[word].append(list_of_chats[index])

        return frequent_question_dict
                


        #stored in form of [number of occurences, list of string associated with keyword]
        


    def close(self) -> bool:
        if self.client is None:
            return False
        
        self.client.close()
        return True

if __name__=="__main__":
    test = Dashboard()
    
    print(test.get_average_response_time())
    print(test.usage_in_past_30_days())
    print(test.get_total_negative_feedback())
    print(test.get_total_positive_feedback())
    print(test.get_percentage_of_positive_feedback())
    print(test.get_all_positive_comments())
    print(test.get_all_negative_comments())
    print(test.get_rating_count())
    print(test.get_solved_response_percentage())
    print(test.get_unsolved_response_percentage())
    print(test.get_accurate_response_percentage())
    print(test.get_inaccurate_response_percentage())
    print(test.get_average_conversation_time())
    print(test.get_top5_most_frequent_question())
    print(test.get_weekly_usage())
    print(test.get_all_questions())

