import spacy
import re
import collections
from spacy import displacy
import graphviz
import matplotlib.pyplot as plt
import networkx as nx

def printFraph(doc):
    a = []
    b = []
    c = {}
    for token in doc:
        if (str(token.text) == ',' or str(token.text) == '.'):
            continue
        print("Token:", token.text)
        print("Head Token:", token.head.text)
        print("Dependency Label:", token.dep_)

        if (str(token.text) != str(token.head)):
            a.append((str(token.text), str(token.head.text), str(token.dep_)))
            b.append([str(token.text), str(token.head.text)])
            c[(str(token.text), str(token.head.text))] = str(token.dep_)
    edges = b
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1, node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in
                    G.nodes()})
    nx.draw_networkx_edge_labels(G, pos, edge_labels=c,
                                 font_color='red')
    plt.axis('off')
    # Сохраняем график в формате PNG
    plt.savefig("graph.png", format="PNG")
    plt.show()


with open('Подлежащие и сказуемые.txt', 'r', encoding='utf-8') as file:
    subVer = file.read().replace('\ufeff', '')

list = subVer.split('\n')
listSubVer = []
for i in list:
    listSubVer.append(i.strip())

# Загрузка модели русского языка
nlp = spacy.load("ru_core_news_sm")
text = ""
# Ваш текст
with open('Дачница.txt', 'r', encoding='utf-8') as file:
    text = file.read()

lines = re.split(r'(?<=[.!?…])\s', text)


with open('Сравнение.txt', 'w') as file:
    file.write('')

countCorrect = 0
value = 0
partCor = 0
for i in range(len(lines)):
    line = lines[i].replace('…', ' ')
    line = line.replace('«', ' ')
    line = line.replace('»', ' ')
    line = line.replace('!', '.')
    # Обработка текста с помощью SpaCy
    doc = nlp(line)

    if (value < 2):
        # Визуализируйте синтаксическое дерево
        png = displacy.render(doc, style="dep", jupyter=False, options={"compact": True})

        # Сохраните визуализацию в файл
        with open("syntax_tree" + str(value) + ".html", "w", encoding="utf-8") as file:
            file.write(png)
        printFraph(doc)

    # Извлечение подлежащих и сказуемых
    subjects = []
    predicates = []

    for token in doc:
        if "nsubj" in token.dep_:
            subjects.append(token.text)

        if ("appos" in token.dep_ and ("PROPN" in token.pos_ or "NOUN" in token.pos_)):
            subjects.append(token.text)

        if ("conj" in token.dep_ and "NOUN" in token.pos_):
            subjects.append(token.text)

        if "ROOT" in token.dep_:
            predicates.append(token.text)
        print(token.text + '    ' + str(token.pos_) + '  ' + str(token.tag_))

    # Вывод результатов
    print("Подлежащие:", subjects)
    print("Сказуемые:", predicates)

    s, v = listSubVer[i].split(',')
    subCor = s.split(' ')
    verbCor = v.split(' ')
    verbCor.remove('')
    print("Корректные подлежащие", subCor)
    print("Корректные сказуемые", verbCor)
    print('\n')

    a = []
    for i in subjects:
        a.append(i.lower())
    subjects = a
    a = []
    for i in predicates:
        a.append(i.lower())
    predicates = a
    a = []
    for i in subCor:
        a.append(i.lower())
    subCor = a
    a = []
    for i in verbCor:
        a.append(i.lower())
    verbCor = a
    a = []

    if (collections.Counter(subjects) == collections.Counter(subCor)):
        if (collections.Counter(predicates) == collections.Counter(verbCor)):
            partCor += 1
        else:
            partCor += 0.5
    elif (collections.Counter(predicates) == collections.Counter(verbCor)):
        partCor += 0.5

    strsub = ""
    for i in subjects:
        strsub += str(i) + ' '
    if len(subjects) == 0:
        strsub += "\t"
    strver = ""
    for i in predicates:
        strver += str(i) + ' '
    if len(predicates) == 0:
        strver += "\t"
    strSubCor = ""
    for i in subCor:
        strSubCor += str(i) + ' '
    if len(subjects) == 0:
        strSubCor += "\t"
    strVerCor = ""
    for i in verbCor:
        strVerCor += str(i) + ' '
    if len(predicates) == 0:
        strVerCor += "\t"

    # Открываем файл для дозаписи (создается, если не существует)
    with open('Сравнение.txt', 'a') as file:
        # Строки для дозаписи
        lines_to_append = ["nsubj: " + str(strsub) + '\t' + "Подлежащее: " + strSubCor + '\n']
        # Записываем строки в файл
        file.writelines(lines_to_append)
        lines_to_append = ["ROOT: " + str(strver) + '\t' + "Сказуемое: " + strVerCor + '\n']
        lines_to_append += 'Доля корректности: ' + str(partCor) + '\n'
        # Записываем строки в файл
        file.writelines(lines_to_append)
        file.writelines('\n')
    # Файл будет автоматически закрыт после блока with
    value += 1
    countCorrect += partCor
    partCor = 0

with open('Сравнение.txt', 'a') as file:
    file.write('Доля корректных данных: ' + str(countCorrect / value * 100) + '%')
print('Доля корректных данных: ' + str(countCorrect / value * 100) + ' %')