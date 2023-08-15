import streamlit as st
import speech_recognition as sr
import string
import cv2
import numpy as np
from moviepy.editor import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import sys

#TO CONCATENATE VIDEOS
def conc_video(video_paths,output_path,method="reduce"):
    
    clips = []
    for c in video_paths:
        
        try:
            clip = VideoFileClip(c)
            clips.append(clip)
        except OSError as e:
            w = c.split('/')[-1].split('.')[0]
            clist = list(w)
            clist[0] = clist[0].lower()
            
            for i in clist:
                
                video_file = 'letters/{}.mp4'.format(i)
                letter_video = VideoFileClip(video_file)
                letter_video = letter_video.crossfadein(2.0)
                clips.append(letter_video)
    
    if method == "reduce":
        min_h = min([c.h for c in clips])
        min_w = min([c.w for c in clips])
        clips = [c.resize(newsize=(min_w,min_h)) for c in clips]
        final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path)
    
#TO GET THE VIDEO PATHS FOR THE CORRESPONDING WORD FROM THE WEBSITE      
def get_video_path(text_list):
    try:
        video_paths = []
        for i in text_list:
            i = i.capitalize()
            path = "http://talkinghands.co.in/sites/default/files/islvideos/{}.webm".format(i)
            video_paths.append(path)
        return video_paths    
    except:
        print("path not avilable")
        
        
#TO GET THE ISL TEXT OF THE ENGLISH TEXT USING ISL GRAMMAR RULES
def get_isl_text(text):
        

    text.lower()
    #tokenizing the sentence
    words = word_tokenize(text)

    tagged = nltk.pos_tag(words)
    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
    tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



    #stopwords that will be removed
    stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])



    #removing stopwords and applying lemmatizing nlp process to words
    lr = WordNetLemmatizer()
    filtered_text = []
    for w,p in zip(words,tagged):
        if w not in stop_words:
            if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
                filtered_text.append(lr.lemmatize(w,pos='v'))
            elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
                filtered_text.append(lr.lemmatize(w,pos='a'))

            else:
                filtered_text.append(lr.lemmatize(w))


    #adding the specific word to specify tense
    words = filtered_text
    temp=[]
    for w in words:
        if w=='I':
            temp.append('Me')
        else:
            temp.append(w)
    words = temp
    probable_tense = max(tense,key=tense.get)

    if probable_tense == "past" and tense["past"]>=1:
        temp = ["Before"]
        temp = temp + words
        words = temp
    elif probable_tense == "future" and tense["future"]>=1:
        if "Will" not in words:
                temp = ["Will"]
                temp = temp + words
                words = temp
        else:
            pass
    elif probable_tense == "present":
        if tense["present_continuous"]>=1:
            temp = ["Now"]
            temp = temp + words
            words = temp
    return words

#TO DISPLAY THE VIDEO 
def display_video():
    st.video('final_video.mp4')
    
#TO RECOGNIZE THE AUDIO INPUT 
def func_speech():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            
            st.write('English Text : {}'.format(text))
            isl_text = []
            isl_text = get_isl_text(text) 
            isl_string = " "
            st.write('ISL text : {}'.format(isl_string.join(isl_text)))
            
            
            # get list of path for all the words
            
            video_path = get_video_path(isl_text)
            
            
            output_path = "final_video.mp4"
            # concatenate the videos of all the words
            
            conc_video(video_path, output_path)
            
            display_video()
            
            os.remove("final_video.mp4")
            
            
            
                
        except:
            st.write('Sorry Not Audible')
                
            

st.title('AUDIO TO SIGN LANGUAGE TRANSLATOR')
st.image('hand-signs-featured-image-1024x576.png')
speak = st.button('Click here to speak')
stop = st.button("Click here to quit")
if speak:
    st.write("Listening")

    func_speech()
if stop:
    st.write(" Thank You ")    
    try: 
        quit()
    except: 
        pass    