from collections import Counter, defaultdict
import json
import string


def read_corpus_from_file(filename):

    with open(filename, 'r') as f:
        corpus = [
            line.strip().translate(str.maketrans('', '', string.punctuation.replace('-', '').replace(',', ''))).split()
            for line in f]
    return corpus



def calculate_word_probabilities(corpus):

    word_counts = {}
    total_words = 0

    for sentence in corpus:
        for word in sentence:
            total_words += 1
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

    word_probabilities = {word: count / total_words for word, count in word_counts.items()}

    return word_probabilities



def word_probabilities_with_context(corpus_file, context_length, output_file):

    corpus = read_corpus_from_file(corpus_file)

    context_counts = defaultdict(Counter)

    for sentence in corpus:
        sentence = [None] * context_length + sentence

        for i in range(context_length, len(sentence)):
            word = sentence[i]
            context = tuple(sentence[i - context_length:i])

            context_counts[context][word] += 1

    probabilities = {}
    k = 0
    for context, word_count in context_counts.items():
        total_count = sum(word_count.values())
        probabilities[context] = {word: count / total_count for word, count in word_count.items()}
    with open('wrdnew.json') as json_file:
        dic1 = json.load(json_file)


    with open(output_file, 'w') as f:
        for context, word_probabilities in probabilities.items():
            context_string = " ".join(str(w) for w in context)
            t = 0
            for word, probability in word_probabilities.items():
                dic1[word].append({"": ""})
                dic1[word][2].update({context_string: [word, probability * 10 ** 5]})

        k = 1;
        jst = json.dumps(dic1)
        f.write(jst)

    return probabilities

#"""
  #  Takes in a filename for the corpus (where each line represents a sentence and words are separated by spaces)
    #and outputs a probability distribution of each word's occurrence given its previous word(s) up to a certain context length.
    #Saves the probability distribution in a text file.
   # """

# Increment the count for this word given its previous context
#  # Convert the counts to probabilities
  # Save probabilities to file

corpus_file = "corpus1.txt"
context_length = 1
output_file = "wrdnew.json"

corpus = read_corpus_from_file(corpus_file)
print(corpus[1])
dic = dict()
word_probabilities = calculate_word_probabilities(corpus)
with open(output_file, 'w') as f:
    for word, probability in word_probabilities.items():
        dic.update({word: [word, probability * 10 ** 5]})
    jst = json.dumps(dic)
    f.write(jst)
word_probabilities_with_context(corpus_file, 1, output_file)

