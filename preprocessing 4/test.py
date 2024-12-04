import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from pymystem3 import Mystem

import numpy as np
from scipy.optimize import curve_fit

# Функция, описывающая формулу Зипфа
def zipf_law(r, c, s):
    return c / (r ** s)


# Используем Mystem для лемматизации русского текста
mystem = Mystem()

text = ""
with open('CrimeAndPunishment.txt', 'r', encoding='utf-8') as file:
    text += file.read() + "\n"
with open('EugeneOnegin.txt', 'r', encoding='utf-8') as file:
    text += file.read() + "\n"
with open('FathersAndSons.txt', 'r', encoding='utf-8') as file:
    text += file.read() + "\n"
with open('MasterAndMargarita.txt', 'r', encoding='utf-8') as file:
    text += file.read() + "\n"
with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
    text += file.read()

# Разбить текст на слова
words = word_tokenize(text, language='russian')

# Разбить текст на слова и произвести лемматизацию
words = [word.lower() for word in word_tokenize(text, language='russian') if word.isalpha()]
ccount = len(words)
print('Общее количество слов: ' + str(len(words)))
lemmas = mystem.lemmatize(" ".join(words))
lemmas = [lemma for lemma in lemmas if lemma.isalpha()]

# Подсчет частоты встречаемости
freq_dist = FreqDist(lemmas)

sorted_freq_dist = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)

s = 0
a = 0
ranks = []
rank = 0
post_rank = 5000000
frequencies = []
ranksReg = []
frequencyReg = []
Graph = {}
with open('Леммы.txt', 'w', encoding='utf-8') as file:
    for r, (lemma, frequency) in enumerate(sorted_freq_dist, 1):
        if (post_rank != frequency):
            rank += 1
            post_rank = frequency
            Graph[rank] = frequency
        file.write("Ранг" + str(rank) + ": Лемма \"" + str(lemma) + "\" с частотой " + str(frequency / ccount) + "\n")
        ranksReg.append(rank)
        frequencyReg.append(frequency)


        if (a < 100):
            ranks.append(rank)
            frequencies.append(frequency / ccount)
        a += 1
        s += (frequency * rank) / ccount

s = s / a
print('Количество уникальных лемм: ' + str(len(sorted_freq_dist)))

# Используем curve_fit для оценки параметров c и s
params, covariance = curve_fit(zipf_law, ranks, frequencies)

c_estimated, s_estimated = params

print(f"Оценка постоянной Зипфа (c): {c_estimated}")
print(f"Оценка показателя степени (s): {s_estimated}")

graphRanks = []
graphFrequency = []
with open('Ранги.txt', 'w', encoding='utf-8') as file:
    for i in Graph.keys():
        graphRanks.append(i)
        graphFrequency.append(Graph[i])
        file.write('Ранг: ' + str(i) + ' общее число слов: ' + str(Graph[i]) + '\n')

plt.figure(figsize=(12, 6))
plt.bar(graphRanks, graphFrequency)
plt.xlabel('Ранг')
plt.ylabel('Частота')
plt.title('Диаграмма Зипфа')
plt.show()
