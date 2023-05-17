import re
import numpy as np
from collections import Counter
import tkinter as tk
import string
from tkinter import *


def words(text):
    return re.findall(r'\w+', text.lower())


def train(features):
    model = Counter(features)
    return model


def edits1(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word, NWORDS):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words, NWORDS):
    return set(w for w in words if w in NWORDS)


def correct(word, NWORDS):
    candidates = known([word], NWORDS) or known(edits1(word), NWORDS) or known_edits2(word, NWORDS) or [word]
    return max(candidates, key=lambda w: NWORDS[w])


def spell_corrector(text, NWORDS):
    corrected_text = []
    for word in re.findall(r'\w+', text.lower()):
        if word not in NWORDS:
            corrected_word = correct(word, NWORDS)
            if corrected_word != word:
                corrected_text.append(corrected_word)
            else:
                corrected_text.append(word)
        else:
            corrected_text.append(word)
    return ' '.join(corrected_text)


def corrector():
    test_text = input_text.get("1.0", "end-1c")
    output_text.delete("1.0", "end")
    with open('big.txt', 'r') as f:
        text = f.read()
    NWORDS = train(words(text))
    corrected_text = spell_corrector(test_text, NWORDS)
    output_text.insert("end", corrected_text + " ")


import string
from tkinter import *


def damerau_levenshtein_distance(s1, s2):
    d = {}
    len_s1 = len(s1)
    len_s2 = len(s2)
    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j + 1
    for i in range(len_s1):
        for j in range(len_s2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 2
            d[(i, j)] = min(d[(i - 1, j)] + 1,  # deletion
                            d[(i, j - 1)] + 1,  # insertion
                            d[(i - 1, j - 1)] + cost)  # substitution
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition
    return d[(len_s1 - 1, len_s2 - 1)]


def generate_candidate_words(word, max_distance):
    letters = string.ascii_lowercase
    candidate_words = set()
    for i in range(len(word)):
        for letter in letters:
            new_word = word[:i] + letter + word[i + 1:]
            distance = damerau_levenshtein_distance(word, new_word)
            if distance <= max_distance:
                candidate_words.add(new_word)
    for i in range(len(word) - 1):
        new_word = word[:i] + word[i + 1] + word[i] + word[i + 2:]
        distance = damerau_levenshtein_distance(word, new_word)
        if distance <= max_distance:
            candidate_words.add(new_word)
    for i in range(len(word) + 1):
        for letter in letters:
            new_word = word[:i] + letter + word[i:]
            distance = damerau_levenshtein_distance(word, new_word)
            if distance <= max_distance:
                candidate_words.add(new_word)
    return candidate_words


def setup_tags():
    output_text.tag_configure("blue_tag", foreground="blue")
    output_text.tag_configure("red_tag", foreground="red")


def on_button_click():
    text = input_text.get("1.0", "end-1c")
    output_text.delete("1.0", "end")
    dict = []
    f = open("big.txt", "r")
    for wor in f:
        wor = wor.split("\n")[0]
        dict.append(wor)
    f.close()
    sent = text
    words = sent.split(" ")
    for word in words:
        print(word, ":")
        max_distance = 2
        candidate_words = generate_candidate_words(word, max_distance)
        if (word in dict):
            output_text.insert("end", word + " ")
        else:
            k = 0
            for i in dict:
                if (i in candidate_words):
                    output_text.insert("end", word + " ", "red_tag")
                    # print(i)
                    k = 1
                    print("incorrect")
                    break
            if (k == 0):
                output_text.insert("end", word + " ", "blue_tag")
                print("unknown")






if __name__ == '__main__':
    root = tk.Tk()
    root.title("Spell Checker")

    root.configure(background='orange')

    root.geometry("800x800+100+100")
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New')
    filemenu.add_command(label='Open...')
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')



    txt = Label(root, text='Enter the text',font=20)
    txt.pack()

    Font_tuple = (" Times New Roman", 25, "italic")
    input_text = tk.Text(root, height=8, width=40)
    input_text.configure(font=Font_tuple)
    input_text.pack()


    submit_button = tk.Button(root, text="Correct",font=20,command=corrector)
    submit_button2 = tk.Button(root, text="Check",font=20, command=on_button_click)
    submit_button2.pack()
    submit_button.pack()

    txt = Label(root, text='spell checker',font=20)
    txt.pack()


    output_text = tk.Text(root, height=8, width=40)
    output_text.configure(font=Font_tuple)
    output_text.pack()

    setup_tags()

    root.mainloop()

# Thsi is an exapmle of a paragarph with sevral mestaks. The spelcheker shuld be able to corect all of the mistaks and produca more accurat vershion of the paragraf.