import json
from queue import PriorityQueue
import io
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import enchant
from tkinter import messagebox
import random

os = io.StringIO()


def edits1(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1)) | set(deletes + transposes + replaces + inserts)


def get_maincan(word, dict, n):
    can_words = list(edits1(word))
    mwords = []
    for i in can_words:
        if (dict.get(i) != None):
            if(i[0]==word[0]):
                mwords.append(dict.get(i)[0])
    if (n == 1):
        return mwords
    can_words = list(edits2(word))
    for i in can_words:
        if (dict.get(i) != None):
            if (i[0] == word[0]):
                mwords.append(dict.get(i)[0])
    return mwords


def pq(words):
    q = PriorityQueue()
    for i in words:
        q.put(dic.get(i[0])[0], dic.get(i[0])[1])
    print(q)


def readDict(a):
    with open(a) as json_file:
        text = json.load(json_file)
    return text


# print((dic.get("the"))[2].get("like")[1] * (dic.get("like"))[2].get("and")[1])
def checker(word):
    if (dic.get(word) != None):
        print("correct")
    else:
        a = get_maincan(word, dic)
        if (len(a) == 0):
            print("no idea")
        else:
            print("wrong")


def get_trigrams(sentence):
    words = sentence.split()
    triples = []
    before_before_word = "!@#"
    before_word = "!@#"
    for i, word in enumerate(words):
        if before_word.endswith('.'):
            if i != len(words) - 1:  # if it's not the last word
                before_before_word = "!@#"
                before_word = "!@#"
        elif word.endswith(','):
            word = word.replace(",","")
        if i == len(words) - 1:  # if it's the last word in the sentence
            triple = [before_before_word, before_word, word]
        else:
            if before_word is not None:
                if before_word.endswith('.'):
                    before_before_word = "!@#"
            triple = [before_before_word, before_word, word]
        if triple[2] is not None:
            triples.append(triple)
        before_before_word = before_word
        before_word = word
    return triples


# defination of dictionaries

dic = readDict("wrd1.json")
dic2 = readDict("wrd.json")


def getSuggested(word, prr, n):
    cou = get_maincan(word, dic, n)
    sugg = []
    for j in cou:
        k = (dic.get(j)[2]).get(prr)
        if (k != None):
            sugg.append((k[1] * -1, j))
    return sorted(sugg)[:4]


def getSuggestedtri(trip, n):
    prev = trip[0] + " " + trip[1]
    # print(prev)
    cou = get_maincan(trip[2], dic2, n)
    sugg = []
    for j in cou:
        k = (dic2.get(j)[2]).get(prev)
        if (k != None):
            sugg.append(k)
    return sugg


def max_word(word):
    can = get_maincan(word, dic, 1)
    prob = []
    for i in can:
        prob.append([dic.get(i)[1], i])
    return prob

def corrector(sentence):
    cor = ""
    trigrams = get_trigrams(sentence)
    k = 1
    for trip in trigrams:
        trip[0] = trip[0].replace(".", "")
        trip[1] = trip[1].replace(".", "")
        trip[2] = trip[2].replace(".", "")
        if (trip[0] != "!@#" and trip[1] != "!@#"):
            trip[1] = cor.split(" ")[-2]
            trip[0] = cor.split(" ")[-3]
        if (trip[0] == "!@#" and trip[1] != "!@#"):
            trip[1] = cor.split(" ")[-2]
        if (trip[1] == "!@#"):
            if (dic.get(trip[2]) != None):
                cor = cor + trip[2] + " "
            else:
                prob = getSuggested(trip[2], 'None', 1)
                if (len(prob) == 0):
                    sugg = max_word(trip[2])
                    if (len(sugg) == 0):
                        cor = cor + trip[2] + " "
                    else:
                        cor = cor + max(sugg)[1] + " "
                        print(trip[2], " : ", sugg)
                else:
                    cor = cor + min(prob)[1] + " "

        else:
            if (trip[0] == "!@#"):
                if (dic.get(trip[2]) != None):
                    cor = cor + trip[2] + " "
                else:
                    prob = getSuggested(trip[2], trip[1], 1)
                    if (len(prob) == 0):
                        sugg = max_word(trip[2])
                        if (len(sugg) == 0):
                            cor = cor + trip[2] + " "
                        else:
                            cor = cor + max(sugg)[1] + " "
                    else:
                        cor = cor + min(prob)[1] + " "


            else:
                if (dic.get(trip[2]) != None):
                    sugg=getSuggestedtri(trip,2)
                    if(len(sugg)==0):
                        cor=cor+trip[2]+" "
                        # sugg=getSuggested(trip[2],trip[1],2)
                        # if(len(sugg)==0):
                        #     cor=cor+trip[2]+" "
                        # else:
                        #     cor=cor+ str(outsug(sugg)[0])+" "
                    else:
                        print("try success")
                        cor=cor+ str(outsug(sugg)[0])+" "

                else:
                    prob = getSuggestedtri(trip, 2)

                    if (len(prob) == 0):
                        prob = getSuggested(trip[2], trip[1], 1)
                        if (len(prob) == 0):
                            sugg = max_word(trip[2])
                            if (len(sugg) == 0):
                                cor = cor + trip[2] + " "
                            else:
                                cor = cor + max(sugg)[1] + " "
                                print(trip[2], " : ", sugg)
                        else:
                            cor = cor + str(min(prob)[1]) + " "
                    else:
                        cor = cor + str(prob[0][1]) + " "

    return cor


def is_corrected(sentence):
    corrected_sentence = corrector(sentence)
    return sentence == corrected_sentence


def outsug(sugg):
    arr=[]
    for i in sugg:
        arr.append(i[1])
    return arr

def suggestor(sentence):
    cor = ""
    ss = ""
    opt=" "

    trigrams = get_trigrams(sentence)
    k = 1
    for trip in trigrams:
        trip[0] = trip[0].replace(".", "")
        trip[1] = trip[1].replace(".", "")
        trip[2] = trip[2].replace(".", "")
       # print(cor.split(" "))
        if (trip[0] != "!@#" and trip[1] != "!@#"):
            trip[1] = cor.split(" ")[-2]
            trip[0] = cor.split(" ")[-3]
        if (trip[0] == "!@#" and trip[1] != "!@#"):
            trip[1] = cor.split(" ")[-2]
        #print(trip)
        if (trip[1] == "!@#"):
            if (dic.get(trip[2]) != None):
                cor = cor + trip[2] + " "
                sugg = getSuggested(trip[2], 'None', 2)
                # cor=cor+sugg      have to setup suggested in gui
                #print(trip[2], " : ", sugg, file=os)
                opt += "{} : {}\n\n".format(trip[2],outsug(sugg), file=os)
                ss = ss + os.getvalue()
            else:
                prob = getSuggested(trip[2], 'None', 1)
                if (len(prob) == 0):
                    sugg = max_word(trip[2])
                    if (len(sugg) == 0):
                        cor = cor + trip[2] + " "
                    else:
                        cor = cor + max(sugg)[1] + " "

                    # print(trip[2]," : ",sugg)
                else:
                    cor = cor + min(prob)[1] + " "
                    sugg = getSuggested(trip[2], 'None', 2)
                # cor=cor+sugg      have to setup suggested in gui
               # print(trip[2], " : ", sugg, file=os)
                opt += "{} : {}\n\n".format(trip[2],outsug(sugg), file=os)
                ss = ss + os.getvalue()
                # print("cor",cor)
        # print("prob",sorted(prob)[:4])
        else:
            if (trip[0] == "!@#"):
                if (dic.get(trip[2]) != None):
                    cor = cor + trip[2] + " "
                    sugg = getSuggested(trip[2], trip[1], 2)
                    #print(trip[2], " : ", sugg, file=os)
                    opt += "{} : {}\n".format(trip[2],outsug(sugg), file=os)
                    ss = ss + os.getvalue()
                else:
                    prob = getSuggested(trip[2], trip[1], 1)
                    if (len(prob) == 0):
                        sugg = max_word(trip[2])
                        if (len(sugg) == 0):
                            cor = cor + trip[2] + " "
                        else:
                            cor = cor + max(sugg)[1] + " "

                        # print(trip[2]," : ",sugg)
                    else:
                        cor = cor + min(prob)[1] + " "
                        sugg = getSuggested(trip[2], 'None', 2)
                    # cor=cor+sugg      have to setup suggested in gui
                    #print(trip[2], " : ", sugg, file=os)
                    opt += "{} : {}\n\n".format(trip[2],outsug(sugg), file=os)
                    ss = ss + os.getvalue()
            else:
                if (dic.get(trip[2]) != None):
                    cor = cor + trip[2] + " "
                    sugg = getSuggestedtri(trip, 2)
                    # sugg.append(getSuggested(trip[2],trip[1],2))
                    #print(trip[2], " : ", sugg, file=os)
                    opt += "{} : {}\n\n".format(trip[2],outsug(sugg), file=os)
                    ss = ss + os.getvalue()
                else:
                    prob = getSuggestedtri(trip, 1)
                    if (len(prob) == 0):
                        #print("noo matching")
                        prob = getSuggested(trip[2], trip[1], 1)
                        if (len(prob) == 0):
                            sugg = max_word(trip[2])
                            if (len(sugg) == 0):
                                cor = cor + trip[2] + " "
                            else:
                                cor = cor + max(sugg)[1] + " "

                            #print(trip[2], " : ", sugg, file=os)
                            opt += "{} : {}\n\n".format(trip[2],sugg, file=os)
                            ss = ss + os.getvalue()

                        else:
                            cor = cor + min(prob)[1] + " "

                            sugg = getSuggested(trip[2], trip[1], 2)
                            #print(trip[2], " : ", sugg, file=os)
                            opt += "{} : {}\n\n".format(trip[2],outsug(sugg), file=os)
                            ss = ss + os.getvalue()

                    else:
                        cor = cor + str( prob[0][1]) + " "
                        sugg = getSuggested(trip[2], 'None', 2)
                        # cor=cor+sugg      have to setup suggested in gui
                        #print(trip[2], " : ", sugg, file=os)
                        opt += "{} : {}\n\n".format(trip[2],outsug(sugg),file=os)
                        ss = ss + os.getvalue()

                        # print(cor)

    #print(cor)
    #print(ss)
    opt+=ss
    return opt

def on_start():
    nb.select(input_page)

def on_correct_button_click():
    sentence = input_text.get("1.0", "end-1c")

    if is_corrected(sentence):
        nb.select(msg_page)
    else:
       # If the sentence needs correction, display corrected text and suggestions
       corrected_sentence = corrector(sentence)
       output_text.configure(state="normal")
       output_text.delete("1.0", "end")
       output_text.insert("1.0", corrected_sentence)
       output_text.configure(state="disabled")
       # switch to the corrected text page
       nb.select(correct_page)

def on_suggest():
    sentence = input_text.get("1.0", "end-1c")

    suggested_sentence = suggestor(sentence)
    suggest_text.configure(state="normal")
    suggest_text.delete("1.0", "end")
    suggest_text.insert("1.0", suggested_sentence)
    suggest_text.configure(state="disabled")
    # switch to the suggestions page
    nb.select(suggest_page)

def slider(label, txt, count=0, text=''):
    if count >= len(txt):
        count = -1
        text = ''
        label.config(text=text)
    else:
        text = text + txt[count]
        label.config(text=text)
    count += 1
    label.after(100, slider, label, txt, count, text)

def change_color():
    headline_label.config(fg=get_random_color())
    root.after(1000, change_color)

def get_random_color():
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color

# Create the main window
if __name__ == '__main__':
   root = tk.Tk()
   root.title("Spell Corrector")
   root.configure(background='grey')
   root.geometry("800x500")

   txt = 'WELCOME TO SPELL CORRECTOR APPLICATION'
   headlbl = tk.Label(root, text=txt, fg='white', bg='grey', font=200)
   headlbl.pack(pady=10)
   slider(headlbl, txt)

   # Create the notebook widget
   nb = ttk.Notebook(root, width=200, height=200)

   welcome_page=ttk.Frame(nb)
   nb.add(welcome_page, text="Welcome")

   txt = "DON'T LET TYPOS GET IN THE WAY OF YOUR TEXT!!"
   txt1 = "WRITE-CHECK-CORRECT"

   headline1_label = tk.Label(welcome_page, text=txt1, font=("Arial", 15, "bold italic"), fg='Red', padx=5,pady=15)
   headline1_label.pack()

   headline_label = tk.Label(welcome_page, text=txt,font=("Arial",15, "bold"), padx=5,pady=35)
   headline_label.pack()
   slider(headline_label, txt)
   change_color()


   #slider(headline1_label, txt1)
  # change_color_1()

   txt1="Our Spell Checker GUI is the  solution to all your spelling errors. "
   txt2= "Say goodbye to embarrassing typos and errors in your emails and  reports."
   txt3= " You can quickly and easily check the spelling of your text and correct on click."
   txt4= " Whether you're a professional writer or a student,Our spell checker is the perfect tool."
   txt5=" Try it today and experience the confidence that comes with perfect spelling!"
   m1_label = tk.Label(welcome_page, text=txt1 , font=4, padx=5, pady=5)
   m1_label.pack()


   m2_label = tk.Label(welcome_page, text=txt2, font=4, padx=5,pady=5)
   m2_label.pack()

   m3_label = tk.Label(welcome_page, text=txt3, font=4, padx=5,pady=5)
   m3_label.pack()

   m4_label = tk.Label(welcome_page, text=txt4, font=4, padx=5,pady=5)
   m4_label.pack()

   m5_label = tk.Label(welcome_page, text=txt5, font=4, padx=5,pady=5)
   m5_label.pack()

   start_button = tk.Button(welcome_page, text="Begin your Spell Corrector Journey", font=30, fg='black', bg='yellow', relief='groove',
                             command=on_start)  # command=lambda: nb.select(correct_page))
   start_button.pack(pady=15)

   # Create the input page
   input_page = ttk.Frame(nb)
   nb.add(input_page, text="Input")
   nb.pack(expand=True, fill="both")

   # Create the input text box
   Font_tuple= ( " Times New Roman",15)
   input_label = tk.Label(input_page, text="Enter the Text",font=4,borderwidth=1,relief='solid',padx=5,pady=5)
   input_label.pack(pady=15)
   input_text = scrolledtext.ScrolledText(input_page, width=60, height=10)
   input_text.configure(font=Font_tuple)
   input_text.pack()

   # Create the submit button
   submit_button = tk.Button(input_page, text="Correct",font=30,fg='black',bg='light blue',relief='groove',command=on_correct_button_click)#command=lambda: nb.select(correct_page))
   submit_button.pack(pady=15)


   # Create the correct page
   correct_page = ttk.Frame(nb)
   nb.add(correct_page, text="Corrected Text")


   # Create the corrected text box
   output_label = tk.Label(correct_page, text="Corrected Text",font=4,borderwidth=1,relief='solid',padx=5,pady=5)
   output_label.pack(pady=15)
   output_text = scrolledtext.ScrolledText(correct_page, width=60, height=10, state="disabled")
   output_text.configure(font=Font_tuple)
   output_text.pack()

   # Create the suggest page
   suggest_page = ttk.Frame(nb)
   nb.add(suggest_page, text="Suggestions")

   # Create the suggest button
   suggest_button = tk.Button(correct_page, text="Suggest",font=30,fg='black',bg='light blue',relief='groove', command=on_suggest)#lambda: nb.select(suggest_page))
   suggest_button.pack(pady=15)

   # Create the suggestions text box
   suggest_label = tk.Label(suggest_page, text="Suggestions Box",font=4,borderwidth=1,relief='solid',padx=5,pady=5)
   suggest_label.pack(pady=15)
   suggest_text = scrolledtext.ScrolledText(suggest_page, width=60, height=10, state="disabled")
   suggest_text.configure(font=Font_tuple)
   suggest_text.pack()

   msg_page = ttk.Frame(nb)
   nb.add(msg_page, text="Messages")

   #msg_label = tk.Label(msg_page, text="Message text",font=4,borderwidth=1,relief='solid',padx=5,pady=5)
   #msg_label.pack(pady=15)
   '''
   msg_text = scrolledtext.ScrolledText(msg_page, width=60, height=10, state="disabled")
   msg_text.configure(font=Font_tuple)
   msg_text.pack()
   '''

   txt="Hurray!! No Errors in the text. Already corrected."
   msg1_label=tk.Label(msg_page,text=txt,font=4,padx=5,pady=150)
   msg1_label.pack()
   slider(msg1_label, txt)

   # Start the main loop
   root.mainloop()
