import spacy

# Загрузите модель spaCy
nlp = spacy.load("ru_core_news_sm")

# Обработайте текст
text = "Леля NN, хорошенькая двадцатилетняя блондинка, стоит у палисадника дачи и, положив подбородок на перекладину, глядит вдаль. "
doc = nlp(text)

from spacy import displacy

from spacy import displacy

# Визуализируйте синтаксическое дерево
html = displacy.render(doc, style="dep", jupyter=False, options={"compact": True})

# Сохраните визуализацию в файл
with open("syntax_tree.html", "w", encoding="utf-8") as file:
    file.write(html)

# Вы можете затем конвертировать HTML-файл в формат PNG или PS с использованием сторонних инструментов

