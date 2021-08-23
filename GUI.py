import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog

"""
    Speech Recognition code
"""

import speech_recognition as sr
from os import path

def select_file():
    global filename
    filename = filedialog.askopenfilenames(initialdir=".")
    no_of_files = len(filename)
    file_path.config(text=(str(no_of_files)+" files are selected"))
    index = 0
    while no_of_files != 0:
        print(filename[index])
        index = index + 1
        no_of_files = no_of_files - 1
    return filename

def Recognize_multiple_files():
    index = 0
    no_of_files = len(filename)
    while no_of_files != 0:
        Recognize_file_Audio(filename[index])
        index = index + 1
        no_of_files = no_of_files - 1

def Recognize_file_Audio(AUDIO_FILE):
    label6.config(text="")
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        try:
            print("Speech Recognition thinks you said: " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # Generate output file name

        num = len(AUDIO_FILE)
        ind = num - 1
        filename1 = ""
        while AUDIO_FILE[ind] != '.':
            ind = ind - 1
        ind = ind - 1
        while AUDIO_FILE[ind] != '/':
            filename1 = AUDIO_FILE[ind] + filename1
            ind = ind - 1
        filename1 = filename1 + ".txt"
        print(filename1)
        text_file = open("text_output/" + filename1, "w")
        text_file.write("%s" % r.recognize_google(audio))
        label3.config(text="Recognize Completed!!!")
        text_file.close()

"""
    Speech nltk code
"""

import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def select_file_for_nltk():
    global filename
    filename = filedialog.askopenfilenames(initialdir=".")
    no_of_files = len(filename)
    file_path1.config(text=(str(no_of_files)+" files are selected"))
    index = 0
    while no_of_files != 0:
        print(filename[index])
        index = index + 1
        no_of_files = no_of_files - 1
    return filename

def nltk_multiple_files():
    index = 0
    no_of_files = len(filename)
    while no_of_files != 0:
        nltk_file_Audio(filename[index])
        index = index + 1
        no_of_files = no_of_files - 1

def nltk_file_Audio(AUDIO_FILE):
    label6.config(text="")
    text = open(AUDIO_FILE, encoding='utf-8').read()
    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

    # Using word_tokenize because it's faster than split()
    tokenized_words = word_tokenize(cleaned_text, "english")

    # Removing Stop Words
    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    # Lemmatization - From plural to single + Base form of a word (example better-> good)
    lemma_words = []
    for word in final_words:
        word = WordNetLemmatizer().lemmatize(word)
        lemma_words.append(word)

    emotion_list = []
    with open('emotions.txt', 'r') as file:
        for line in file:
            clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
            word, emotion = clear_line.split(':')

            if word in lemma_words:
                emotion_list.append(emotion)

    print(emotion_list)
    w = Counter(emotion_list)
    print(w)

    #Generate output file name

    num = len(AUDIO_FILE)
    ind = num - 1
    filename1 = ""
    while AUDIO_FILE[ind] != '.':
        ind = ind - 1
    ind = ind - 1
    while AUDIO_FILE[ind] != '/':
        filename1 = AUDIO_FILE[ind] + filename1
        ind = ind - 1
    filename1 = filename1 + ".txt"
    print(filename1)
    text_file = open("Analysis/" +filename1, "w")
    text_file.write("%s" % emotion_list)

    sentiment_analyse(cleaned_text)

    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    plt.show()

    label6.config(text="nltk Completed!!!")

def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        print("Negative Sentiment")
    elif score['neg'] < score['pos']:
        print("Positive Sentiment")
    else:
        print("Neutral Sentiment")


"""
    GUI main
"""

root = tk.Tk()
root.title("Recognition System")

#tabs

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Recognition')

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='Analysis')

tabControl.pack(expand=1, fill="both")

#tab 1

header = Label(tab1, text="Select Recognitions files!", font=("Helvetica", 18, 'bold'))
header.pack(side=TOP, expand=YES)

btn1 = Button(tab1, text='Add file', command=select_file, font=("Helvetica", 14))
btn1.pack(side=TOP, expand=YES)

file_path = ttk.Label(tab1, text="None of file selected!", font=("Helvetica", 12, 'italic'))
file_path.pack(side=TOP, expand=YES)

btn2 = Button(tab1, text='Recognize', command=Recognize_multiple_files, font=("Helvetica", 14))
btn2.pack(side=TOP, expand=YES)

label3 = ttk.Label(tab1, text="", font=("Helvetica", 20, 'bold'))
label3.pack(side=TOP, expand=YES)

#tab 2

header1 = Label(tab2, text="Select files for Analysis!", font=("Helvetica", 18, 'bold'))
header1.pack(side=TOP, expand=YES)

btn3 = Button(tab2, text='Add file', command=select_file_for_nltk, font=("Helvetica", 14))
btn3.pack(side=TOP, expand=YES)

file_path1 = ttk.Label(tab2, text="None of file selected!", font=("Helvetica", 12, 'italic'))
file_path1.pack(side=TOP, expand=YES)

btn4 = Button(tab2, text='Analysis', command=nltk_multiple_files, font=("Helvetica", 14))
btn4.pack(side=TOP, expand=YES)

label6 = ttk.Label(tab2, text="", font=("Helvetica", 20, 'bold'))
label6.pack(side=TOP, expand=YES)

root.geometry("500x300")
root.mainloop()