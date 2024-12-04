import nltk

nltk.download('punkt')  # Если вы еще не скачали токенизатор NLTK

from nltk.tokenize import sent_tokenize

text = "Текст вашего рассказа. Второе предложение. Третье предложение. Четвертое предложение."
sentences = sent_tokenize(text, language='russian')

# Теперь у вас есть список предложений
import spacy

nlp = spacy.load("ru_core_news_sm")  # Загрузка модели spaCy для русского языка

results = []

for sentence in sentences:
    doc = nlp(sentence)
    subject = None  # Инициализируем переменные в начале каждого предложения
    predicate = None
    for token in doc:
        if "subj" in token.dep_:
            subject = token.text
        if "pred" in token.dep_:
            predicate = token.text
    results.append((subject, predicate))

# Теперь у вас есть список кортежей, каждый из которых содержит подлежащее и сказуемое для каждого предложения

from spacy import displacy

for i in range(4):
    sentence = sentences[i]
    doc = nlp(sentence)
    displacy.render(doc, style="dep", jupyter=False, options={"compact": True})
    output_file = f"graph_{i+1}.png"
    displacy.serve(doc, style="dep", options={"compact": True, "color": "blue"}, page=False, minify=False)
    displacy.save(doc, output_file)
