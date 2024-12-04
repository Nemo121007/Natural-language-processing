data = ""
with open('CrimeAndPunishment.txt', 'r', encoding='utf-8') as file:
    data += file.read()
with open('EugeneOnegin.txt', 'r', encoding='utf-8') as file:
    data += file.read()
with open('FathersAndSons.txt', 'r', encoding='utf-8') as file:
    data += file.read()
with open('MasterAndMargarita.txt', 'r', encoding='utf-8') as file:
    data += file.read()
with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
    data += file.read()

dict_char = {}
count_char = 0
for char in data:
    count_char += 1
    if char in dict_char:
        dict_char[char] += 1
    else:
        dict_char[char] = 1
sorted_tuples_char = sorted(dict_char.items(), key=lambda x: x[1], reverse=True)
frequency_dict_char = {}
for char, c in sorted_tuples_char:
    frequency_dict_char[char] = c / count_char

a = 0
with open('буквы.txt', 'w', encoding='utf-8') as file:
    file.write('Буквенные символы \n')
    for i in sorted_tuples_char:
        if (str(i[0]).isalpha()):
                file.write(str(i[0] + ' ' + str(i[1])) + '\n')
                a += 1
    file.write('Небуквенные символы\n')
    for i in sorted_tuples_char:
        if (not (str(i[0]).isalpha())):
            file.write(str(i[0] + ' ' + str(i[1])) + '\n')
            a += 1
    file.write('Всего символов: ' + str(a) + '\n\n\n')
    file.write('Частота встречаемости:\n\n\n')
    file.write('Буквенные символы \n')
    for char in frequency_dict_char:
        if (char.isalpha()):
            file.write(char + ' ' + str(frequency_dict_char[char]) + '\n')
    file.write('Небуквенные символы \n')
    for char in frequency_dict_char:
        if not (char.isalpha()):
            file.write(char + ' ' + str(frequency_dict_char[char]) + '\n')

dict_words = {}
words = []
count = 0
i = 0
word = ""
for i in range(len(data)):
    if (data[i].isalpha()):
        word += data[i]
    else:
        if (data[i] == '-' and data[i + 1].isalpha()):
            word += data[i]
        else:
            if (word != ""):
                words.append(word.lower())
                word = ""
            else:
                continue

for word in words:
    if word in dict_words:
        dict_words[word] += 1
        count += 1
    else:
        dict_words[word] = 1
        count += 1

a = 0
sorted_tuples_word = sorted(dict_words.items(), key=lambda x: x[1], reverse=True)
with open('слова.txt', 'w', encoding='utf-8') as file:
    for word in sorted_tuples_word:
        file.write(str(word[0] + '  ' + str(word[1])) + '\n')
        a += 1
    file.write('Всего слов: ' + str(count) + '\n')
    file.write('Уникальных слов: ' + str(a) + '\n')

with open('словарь.txt', 'w', encoding='utf-8') as file:
    for word in sorted_tuples_word:
        file.write(str(word[0]) + "\n")
