import speech_recognition as sr
from pydub import AudioSegment
import wave
import keyboard
from flask.wrappers import Request
from flask import Flask , render_template, request, redirect, url_for, session,Response
import re
import pickle
from flask_mysqldb import MySQL

r = sr.Recognizer()  
paragraph_string = 'This is a cat'
paragraph = paragraph_string.lower()
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

for ele in paragraph:
    if ele in punc:
        paragraph = paragraph.replace(ele, "")

paragraph = list(paragraph.split(" "))
text = 'No text found'

#For Identification of Dyslexia. Small paragraph will be given.
#Paragraph to be mentioned in paragraph_string variable coming from database.
with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data = r.record(source, duration=4)
            print("Recognizing...")
            # convert speech to text
            try :
                text_og= str(r.recognize_google(audio_data, language= "en-IN"))
                text = text_og.lower()
                text = list(text.split(" ")) 
            except :
                pass    
count = 0
for i in range(len(paragraph)):
    for j in range(len(text)):
        if paragraph[i] == text[j]:
            count = count + 1

wrong_words_spoken_list = [] 
right_words_spoken_list = []           
for i in range(len(text)):
    if text[i] in paragraph:
        right_words_spoken_list.append(text[i])
    elif text[i] not in paragraph:
        wrong_words_spoken_list.append(text[i])
        

accuracy = 100* (count/len(paragraph))
print ('Analysis :')
print('Text given to student to read: ', paragraph_string)
print('Text spoken by the Student : ', text_og)
print('The list of right words spoken by the student is: ', right_words_spoken_list) 
print('The list of wrong words spoken by the student is: ', wrong_words_spoken_list) 
print('Accuracy Percentage of right words: ', accuracy)
print('Number of right words spoken: {right} and number of wrong words spoken: {wrong}'.format(right = len(right_words_spoken_list), wrong = len(wrong_words_spoken_list)))  






#For Treatment of Words
with sr.Microphone() as source:
            # read the audio data from the default microphone
            audio_data = r.record(source, duration=4)
            print("Recognizing...")
            # convert speech to text
            try :
                text = str(r.recognize_google(audio_data, language= "en-IN"))
                text = text.lower()
                print(text) 
                print(len(text))
            except :
                pass    
word = ['cat', 'dog', 'this', 'that', 'boy', 'girl', 'animal']

if text in word:
       print('Correct Recitation of word was done by the student')
else :
       print('Inorrect Recitation of word was done by the student')


#For treatment of Phrases / Sentences / Paragraphs :
#same as identification
