'''
Alexa Custom Skill to enable voice control of your tv using a Raspberry Pi
    - Uses flask-ask and irsend on raspberry pi
Usage:
Alexa, tell my tv to turn on/off
Alexa, tell my tv to increase/decrease/mute the volume
Alexa, tell my tv to switch to channel 95
Alexa, tell my tv to channel surf up/down
Created by: Lee Assam
www.powerlearningacademy.com
Last Modified: 2018-07-20
'''
from flask import Flask, render_template
from flask_ask import Ask, statement, question, request, session, convert_errors
import os, time

#initialize the app
app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def start_skill():
    welcome_message = render_template('Hello Everyone!')
    return question(welcome_message)

@ask.intent('AMAZON.HelpIntent')
def help():
    return start_skill()

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    fallback_message = render_template('fallback_message')
    return statement(fallback_message)

@ask.session_ended
def session_ended():
    return "{}", 200

#Introduce me
@ask.intent('SomethingAboutMe')
def somethingAboutMe():
    text = "Hello Everyone! I am Alexa, Omkar's Virtual Assistant. He lives in Ulhasnagar, Thane. He is currently pursuing a Bachelors Degree in Electronics Engineering from Mumbai University. He likes programming, learning new technical things. He spends most of his time watching youtube videos. His area of interests are Competetive Programming, PC Building, and International Relations. He is very excited to be a part of the LTI family and Thankful to Niranjan sir for allowing him to introduce himself."
    return statement(text)

if __name__ == '__main__':
    app.run(debug=True)
