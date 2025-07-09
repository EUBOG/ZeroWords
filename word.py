import requests
from bs4 import BeautifulSoup
from googletrans import Translator

def get_english_words():
    url = "https://randomword.com/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    try:
        # Устанавливаем таймаут
        response = requests.get(url, headers=headers, timeout=(300, 300))
        # Проверяем успешность запроса
        if response.status_code != 200:
            print("Не удалось загрузить страницу")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        english_word = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()

        return {
            "english_words": english_word,
            "word_definition": word_definition
        }

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def word_game():
    print("Добро пожаловать в игру!")
    while True:
        word_dict = get_english_words()

        # Проверяем, успешно ли получено слово
        if not word_dict:
            print("Не удалось получить слово. Попробуем ещё раз?")
            play_again = input("Хотите попробовать ещё раз? y/n: ")
            if play_again.lower() != "y":
                break
            continue

        word = word_dict["english_words"]
        definition = word_dict["word_definition"]

        print(f"\nЗначение слова: {definition}")
        user_input = input("Какое это слово? ")

        if user_input.lower() == word.lower():
            print("✅ Правильно!")
        else:
            print(f"❌ Неверно. Загаданное слово: {word}")

        play_again = input("\nХотите сыграть ещё раз? y/n: ")
        if play_again.lower() != "y":
            print("Спасибо за игру!")
            break


# Запуск игры
if __name__ == "__main__":
    word_game()