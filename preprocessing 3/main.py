import csv

separators = ["Посвящ", "Случай первый", "Случай другой", "Случай третий", "Глава", "Заключение", "«", "I",
              "Часть первая", "Часть вторая", "Части второй", "Действие первое", "Действие второе", "…", "?..",
              "По русскому языку", "* * *", "* * *", "ВЕРХ", "Марка в 60 к.","действи", "I", "Пролог", "Эпилог",
              "Гамлет", "Нар. песня", "\tКуда, милай, скрылся?", "…лукавых простаков,", "Грибоедов",
              "О марте", "Об апреле", "О мае","Об июне и июле", "Об августе", "(Продолжение до nec plus ultra).",
              "Навозну кучу разрывая,", "Крылов"]

def SearchSeparators(story):
    if ("«Врач»" in story) or ("Эпизодик" in story) or ("«Кавардак в Риме»" in story) \
            or ("«О марте. Об апреле. О мае. Об июне и июле. Об августе»" in story)\
            or ("О том, о сем" in story) or ("\n\nОткрытие" in story):
        return False
    for sep in separators:
        if sep in story:
            return True
    return False

# Открываем файл с неструктурированным текстом
with open('Чехов - рассказы.txt', 'r', encoding='utf-8') as file:
    text = file.read()

indexCopy = 0
count = 0
for i in range(len(text)):
    if (text[i] == '©'):
        indexCopy = i
        break
for i in range(indexCopy + 1, len(text)):
    if (text[i] == '\n'):
        indexCopy = i
        count += 1
        if (count == 4):
            break
text = text[indexCopy + 1:].replace("     ", '\t')
text = text.replace("\n\t\n\t", "\n\t")
with open("тест\\Словарь" + '.txt', 'w', encoding='utf-8') as file:
    file.write(text)

stories_lists = text.split('\n\t\n\t\n')

stories = []
for stories_page in stories_lists:
    stor = stories_page.split("\n\t\n")
    for strl in stor:
        nd = strl.split("\n\n\n")
        for n in nd:
            stories.append(n)
#i = 52
i = 0
while i < len(stories):
    s = ""
    for j in range(len(stories[i]) - 1):
        if stories[i][j] == "\n":
            break
        s += (stories[i])[j]
    if (SearchSeparators(s)):
        stories[i - 1] += "\n\n" + stories[i]
        stories.remove(stories[i])
        continue
#    s = stories[i]
#    if (stories[i] == "Жених и папенька\n(Нечто современное)" ):
#        stories[i] += "\n\n" + stories[i + 1]
#        stories.remove(stories[i + 1])
#        continue
#    if ("(Продолжение до nec plus ultra)." in stories[i]):
#        st = stories[i]
#        st1, st2 = st.split("(Продолжение до nec plus ultra).")
#        stories[i] = st1
#        stories.append(st2)
    i += 1

a = 0
for i in stories:
    with open('тест\\' + str(a) + '.txt', 'w', encoding='utf-8') as file:
        file.write(stories[a])
        a += 1