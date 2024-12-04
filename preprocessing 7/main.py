import spacy
import re
import collections
import matplotlib.pyplot as plt
import networkx as nx
def printFraph(data):
    dictTranslate = {
        "ADJ" : "прилагательное",
        "ADP": "предлог",
        "ADV": "наречие",
        "AUX": "вспомогательный глагол",
        "CONJ": "союз",
        "DET": "артикль",
        "INTJ": "междометие",
        "NOUN": "существительное",
        "NUM": "числительное",
        "PART": "частица",
        "PRON": "местоимение",
        "PROPN": "имя собственное",
        "PUNCT": "пунктуация",
        "CCONJ": "подчинительный союз",
        "SYM": "символ",
        "VERB": "глагол",
        "X": "другое",
        "Начало" : "Начало",
        "Конец" : "Конец"
    }

    dataWord = {}
    for name in data.keys():
        if dictTranslate.keys().__contains__(name[0]) and dictTranslate.keys().__contains__(name[1]):
            dataWord[(dictTranslate[name[0]], dictTranslate[name[1]])] = data[name]

    for n in dataWord.keys():
        name = n[0]
        s = 0
        for line in dataWord.keys():
            if line[0] == name:
                s += dataWord[line]
        for line in dataWord.keys():
            if line[0] == name:
                dataWord[line] = round(dataWord[line] / s, 5)

    with open('Модель языка.txt', 'w', encoding='utf-8') as file:
        for i in sorted(dataWord, key=lambda x: x[0]):
            file.write(i[0] + " - " + i[1] + " : " + str(dataWord[i]) + "\n")

    nodes = []
    for name in dataWord.keys():
        if not nodes.__contains__(name[0]):
            nodes.append(name[0])
        if not nodes.__contains__(name[1]):
            nodes.append(name[1])

    edges = {}
    for line in dataWord.keys():
        edges[line[0], line[1]] = dataWord[line]

    G = nx.DiGraph()
    G.add_edges_from(edges.keys())
    # Упорядочиваем вершины по кругу
    pos = nx.circular_layout(G)
    plt.figure()
    # Рисуем рёбра с подписями
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1, node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in
                    G.nodes()})
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges,
                                 font_color='red')
    plt.axis('off')
    # Сохраняем график в формате PNG
    plt.savefig("graph.png", format="PNG")
    # Показываем граф
    plt.show(block=True)


t = []
#with open('CrimeAndPunishment.txt', 'r', encoding='utf-8') as file:
#    a = file.read().split(".")
#    for i in a:
#        t.append(i)
with open('EugeneOnegin.txt', 'r', encoding='utf-8') as file:
    a = file.read().split(".")
    for i in a:
        t.append(i)
#with open('FathersAndSons.txt', 'r', encoding='utf-8') as file:
#    a = file.read().split(".")
#    for i in a:
#        t.append(i)
#with open('MasterAndMargarita.txt', 'r', encoding='utf-8') as file:
#    a = file.read().split(".")
#    for i in a:
#        t.append(i)
#with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
#    a = file.read().split(".")
#    for i in a:
#        t.append(i)

nlp = spacy.load("ru_core_news_sm")

i = 0
dataWords = {}
for text in t:
    for line in nlp(str(text)).sents:
        if i > 30:
           break
        i += 1
        doc = nlp(str(line))
        flagFirst = True
        firstWorld = ""
        pastWorld = ""
        for word in doc:
            if flagFirst:
                firstWorld = word.pos_
                flagFirst = False
            pastWorld = word.pos_
            first = word.pos_
            # Проверка на наличие второго слова
            if word.head is not None:
                second = word.head.pos_
                if dataWords.__contains__((second, first)):
                    dataWords[(second, first)] += 1
                else:
                    dataWords[(second, first)] = 1
        fir = ("Начало", firstWorld)
        if dataWords.__contains__(fir):
            dataWords[fir] += 1
        else:
            dataWords[fir] = 1
        sec = (pastWorld, "Конец")
        if dataWords.__contains__(sec):
            dataWords[sec] += 1
        else:
            dataWords[sec] = 1
printFraph(dataWords)