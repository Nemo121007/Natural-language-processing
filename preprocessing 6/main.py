import spacy
from collections import Counter
from rouge import Rouge
from summa import summarizer
from nltk import ngrams

countSentence = 7


def get_lemmatized_tokens(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if token.is_alpha]
    return tokens


def get_ngrams(tokens, n):
    n_grams = list(ngrams(tokens, n))
    return n_grams


def rouge_n(reference, summary, n):
    reference_tokens = get_lemmatized_tokens(reference)
    summary_tokens = get_lemmatized_tokens(summary)

    reference_ngrams = get_ngrams(reference_tokens, n + 1)
    summary_ngrams = get_ngrams(summary_tokens, n + 1)

    count = 0
    for line in reference_ngrams:
        if line in summary_ngrams:
            count += 1
            summary_ngrams.remove(line)

    return count / len(reference_ngrams)


def CreateDict(words):
    i = 0
    coun = 10
    resultDict = {}
    for line in words:
        if i < coun:
            resultDict[line[0]] = 10 - int(i / 2)
            i += 1
        else:
            resultDict[line[0]] = 0
    return resultDict


# Загрузка модели SpaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

with open("вирус.txt", "r", encoding="utf-8") as file:
    text = file.read().replace("\ufeff", "")

# Обработка текста с использованием SpaCy
doc = nlp(text)

# Лемматизация и удаление стоп-слов
tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]

# Подсчет частоты слов
word_freq = dict(Counter(tokens))
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
word_freq = CreateDict(sorted_word_freq)

# Расчет веса каждого предложения
sentence_weights = {}
text_sentence = []
for sentence in nlp(text).sents:
    text_sentence.append(str(sentence))
    count = 0
    l = 0
    for world in nlp(str(sentence)):
        a = world.lemma_
        if word_freq.__contains__(world.lemma_):
            count += word_freq[world.lemma_]
            l += 1
    sentence_weights[str(sentence)] = count / l

# Сортировка предложений по весу
sorted_sentences = [
    sentence
    for sentence, weight in sorted(
        sentence_weights.items(), key=lambda x: x[1], reverse=True
    )
]


def writeReport(textReport, name):
    search_sentence = set()
    i = 0
    global sorted_sentences

    countSentence = 0
    for sentence in nlp(textReport).sents:
        countSentence += 1

    for line in sorted_sentences:
        if i < countSentence:
            search_sentence.add(str(line).strip())
            i += 1
        else:
            break

    result = ""
    for line in text_sentence:
        if str(line).strip() in search_sentence:
            result += line.strip() + " "

    with open(
        "Реферат  с парамерами " + str(name) + ".txt", "w", encoding="utf-8"
    ) as file:
        file.write(result)

    rouge = Rouge()
    scores = rouge.get_scores(result, textReport)

    # Вывод метрик ROUGE с проверкой наличия метрики ROUGE-3
    print("ROUGE-1 F1 Score:", scores[0].get("rouge-1", {}).get("f", "N/A"))
    print("ROUGE-2 F1 Score:", scores[0].get("rouge-2", {}).get("f", "N/A"))
    print("ROUGE-3 F1 Score:", scores[0].get("rouge-3", {}).get("f", "N/A"))


with open("Вирус-реферат.txt", "r", encoding="utf-8") as file:
    textRef = file.read()
writeReport(textRef, "Образец")

with open("Реферат  с парамерами Образец.txt", "r", encoding="utf-8") as file:
    t = file.read()
print(str("Образец" + " ручной подсчёт "))
for i in range(3):
    try:
        a = rouge_n(textRef, t, i)
        print("ROUGE-" + str(i) + " :" + str(a))
    except:
        print("ROUGE-" + str(i) + " : N/A")

with open("Вирус-реферат- Splitbrain.txt", "r", encoding="utf-8") as file:
    textSplitbrain = file.read()
rouge = Rouge()
scores = rouge.get_scores(textSplitbrain, textRef)

print("\nSplitbrain")
print(str("Splitbrain" + " ручной подсчёт "))
for i in range(3):
    try:
        a = rouge_n(textRef, textSplitbrain, i)
        print("ROUGE-" + str(i) + " :" + str(a))
    except:
        print("ROUGE-" + str(i) + " : N/A")
print("\nБиблиотека")
# Вывод метрик ROUGE с проверкой наличия метрики ROUGE-3
print("ROUGE-1 F1 Score:", scores[0].get("rouge-1", {}).get("f", "N/A"))
print("ROUGE-2 F1 Score:", scores[0].get("rouge-2", {}).get("f", "N/A"))
print("ROUGE-3 F1 Score:", scores[0].get("rouge-3", {}).get("f", "N/A"))

with open("Вирус-реферат-Визуальный мир.txt", "r", encoding="utf-8") as file:
    textNewWorld = file.read()
rouge = Rouge()
scores = rouge.get_scores(textNewWorld, textRef)

print("\nВизуальный мир")
print(str("Визуальный мир" + " ручной подсчёт "))
for i in range(3):
    try:
        a = rouge_n(textRef, textNewWorld, i)
        print("ROUGE-" + str(i) + " :" + str(a))
    except:
        print("ROUGE-" + str(i) + " : N/A")
print("\nБиблиотека")
# Вывод метрик ROUGE с проверкой наличия метрики ROUGE-3
print("ROUGE-1 F1 Score:", scores[0].get("rouge-1", {}).get("f", "N/A"))
print("ROUGE-2 F1 Score:", scores[0].get("rouge-2", {}).get("f", "N/A"))
print("ROUGE-3 F1 Score:", scores[0].get("rouge-3", {}).get("f", "N/A"))


# Создание реферата с использованием summa
a = len(doc) * 0.05
summary = summarizer.summarize(text, words=len(doc) * 0.05)

textSum = str(summary)
rouge = Rouge()
scores = rouge.get_scores(textSum, textRef)

print("\nSumma")
print(str("Summa" + " ручной подсчёт "))
for i in range(3):
    try:
        a = rouge_n(textRef, str(summary), i)
        print("ROUGE-" + str(i) + " :" + str(a))
    except:
        print("ROUGE-" + str(i) + " : N/A")
print("\nБиблиотека")
# Вывод метрик ROUGE с проверкой наличия метрики ROUGE-3
print("ROUGE-1 F1 Score:", scores[0].get("rouge-1", {}).get("f", "N/A"))
print("ROUGE-2 F1 Score:", scores[0].get("rouge-2", {}).get("f", "N/A"))
print("ROUGE-3 F1 Score:", scores[0].get("rouge-3", {}).get("f", "N/A"))
