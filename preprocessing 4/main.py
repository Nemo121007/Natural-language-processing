import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

texts = []
with open('CrimeAndPunishment.txt', 'r', encoding='utf-8') as file:
    texts.append(file.read())
with open('EugeneOnegin.txt', 'r', encoding='utf-8') as file:
    texts.append(file.read())
with open('FathersAndSons.txt', 'r', encoding='utf-8') as file:
    texts.append(file.read())
with open('MasterAndMargarita.txt', 'r', encoding='utf-8') as file:
    texts.append(file.read())
with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
    texts.append(file.read())

# Сегментация текста на слова
words = []
for text in texts:
    words.extend(word_tokenize(text, language='russian'))

count = len(words)

from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("russian")

lemmas = [stemmer.stem(word) for word in words]

freq_dist = FreqDist(lemmas)

# Получите наиболее часто встречающиеся леммы
most_common = freq_dist.most_common(200)  # например, выберем n самых частых лемм
for i in freq_dist.keys():
    print(str(i) + '    ' + str(freq_dist[i]))
# Расчет ранга и построение диаграммы
ranks = list(range(1, len(most_common) + 1))
frequencies = [count for _, count in most_common]

for i in range(len(most_common)):
    print(str(most_common[i]) + '    ' + str(i + 1))

import numpy as np
from scipy import stats

# Преобразование в логарифмические значения
log_ranks = np.log(ranks)
log_frequencies = np.log(frequencies)

# Выполнение линейной регрессии
slope, intercept, r_value, p_value, std_err = stats.linregress(log_ranks, log_frequencies)

# Расчет параметра Зипфа (обратный коэффициент наклона)
zipf_constant = 1 / slope

print("Параметр Зипфа (Зипфовская константа):", zipf_constant)

plt.figure(figsize=(12, 6))
plt.bar(ranks, frequencies)
plt.xlabel('Ранг')
plt.ylabel('Частота')
plt.title('Диаграмма Зипфа')
plt.show()


