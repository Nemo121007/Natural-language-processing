def load_dictionary():
    with open('словарь.txt', 'r', encoding='utf-8') as file:
        return set(line.strip().lower() for line in file)

def is_correct_word(word, dictionary):
    return word in dictionary

def generate_corrections(word):
    corrections = set()

    # Операция вставки буквы
    for i in range(len(word) + 1):
        for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            corrected_word = word[:i] + char + word[i:]
            corrections.add(corrected_word)

    # Операция удаления буквы
    for i in range(len(word)):
        corrected_word = word[:i] + word[i+1:]
        corrections.add(corrected_word)
    # Операция замены буквы
    for i in range(len(word)):
        for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
            corrected_word = word[:i] + char + word[i+1:]
            corrections.add(corrected_word)

    # Операция перестановки соседних букв
    for i in range(len(word) - 1):
        corrected_word = word[:i] + word[i+1] + word[i] + word[i+2:]
        corrections.add(corrected_word)

    return corrections


def main():
    dictionary = load_dictionary()
    user_word = input("Введите слово: ").lower()

    if is_correct_word(user_word, dictionary):
        print(f"Слово '{user_word}' написано правильно.")
    else:
        print(f"Слово '{user_word}' написано неправильно. Возможные исправления:")
        corrections = generate_corrections(user_word)
        for correction in corrections:
            if correction in dictionary:
                print(correction)


if __name__ == "__main__":
    main()
