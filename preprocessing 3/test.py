import csv

def LineIsEmpty(st):
    for i in st:
        if (i == " " or i == "\t" or i == "\n"):
            continue
        else:
            return False
    return True

def CheckExceptions(line):
    for i in list_exceptions:
        if (i in line):
            return True
    return False

def CheckNamesCollections(st):
    for i in NamesCollections:
        if (i in st):
            return True
    return False


def create_dict(lines, names_stories):
    result_dict = {}
    i = 1
    start_name = names_stories[0]
    end_name = names_stories[1]
    st = ""
    for line in lines:
        if (line in end_name) and not (LineIsEmpty(line)):
            result_dict[start_name] = st
            start_name = end_name
            i += 1
            if i < len(names_stories):
                end_name = names_stories[i]
            else:
                end_name = names_stories[0]
            st = ""
            continue
        st += line.strip() + '\n'
    result_dict[start_name] = st

    return result_dict


NamesCollections = ["Шалость", "Из сборника «Пестрые рассказы»", "Сказки Мельпомены"]
list_exceptions = ["Случай первый", "Случай другой", "Случай третий", "Глава", "Заключение", "I",
              "Часть первая", "Часть вторая", "Части второй", "Действие первое", "Действие второе", "По русскому языку",
              "Арифметика", "* * *", "ВЕРХ","Пролог", "Эпилог", "(Продолжение до nec plus ultra)."]
lines = []
mark = True
with open ("Чехов - рассказы.txt", 'r+', encoding="UTF-8") as f:
    for line in f:
        if (mark):
            if ('©' in line):
                mark = False
            continue
        lines.append(line.replace('\n', ''))

names_stories = []
for i in range(len(lines)):
    if (len(lines[i]) != 0):
        if (lines[i][0] == " "):
            continue
        else:
            if (CheckNamesCollections(lines[i])):
                lines[i] = ""
                continue
            if (CheckExceptions(lines[i])):
                continue

            if not (LineIsEmpty(lines[i + 1])):
                names_stories.append(lines[i] + ' ' + lines[i + 1])
                lines[i + 1] = ""
                continue
            else:
                names_stories.append(lines[i])

dictionary_story = create_dict(lines, names_stories)

names_stories.sort()
# Указать имя файла для записи
file_name = "example.csv"
# Открыть файл для записи в режиме 'w', указав newline='', чтобы избежать дополнительных пустых строк
with open(file_name, 'w', newline='\n', encoding="UTF-8") as csv_file:
    # Создать объект для записи CSV
    csv_writer = csv.writer(csv_file)

    # Записать каждую строку в файл
    for name in names_stories:
        csv_writer.writerow([name])
print(f"Список строк записан в файл {file_name}")

name = ""
wrongs = ['\x1e','\xa0','<','>', ":", "?", "|"]
for cort in dictionary_story.keys():
    name = cort.replace('\x1e', ' ')\
        .replace('\xa0', ' ')\
        .replace('?', ' ')\
        .replace('<', '«')\
        .replace('>', '»')
    with open('тест\\' + name + '.txt', 'w', encoding='utf-8') as file:
        file.write(dictionary_story[cort].strip())

print("Рассказы записаны в отдельные файлы")