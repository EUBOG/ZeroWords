import requests
from bs4 import BeautifulSoup
from translate import Translator


def translate_to_russian(text):
    try:
        translator = Translator(from_lang="en", to_lang="ru")
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text


def get_english_words():
    url = "https://randomword.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)

        if not response.ok:
            print(f"Не удалось загрузить страницу. Код статуса: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        english_word = soup.find("div", id="random_word")
        word_definition = soup.find("div", id="random_word_definition")

        if not english_word or not word_definition:
            print("Не найдены элементы со словом или определением на странице")
            return None

        word_en = english_word.text.strip()
        definition_en = word_definition.text.strip()

        # Переводим слово и определение
        word_ru = translate_to_russian(word_en)
        definition_ru = translate_to_russian(definition_en)

        return {
            "english_word": word_en,
            "russian_word": word_ru,
            "definition": definition_ru
        }

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


def word_game():
    print("Добро пожаловать в игру 'Угадай слово'!")
    print("Я дам вам определение слова на русском, а вы попробуете угадать само слово.")

    while True:
        word_dict = get_english_words()

        if not word_dict:
            print("\nНе удалось получить слово. Попробуем ещё раз?")
            play_again = input("Хотите попробовать ещё раз? (да/нет): ").lower()
            if play_again not in ['да', 'д', 'y', 'yes']:
                break
            continue

        english_word = word_dict["english_word"]
        russian_word = word_dict["russian_word"]
        definition = word_dict["definition"]

        print(f"\nОпределение: {definition}")
        user_input = input("Какое это слово? (на русском): ").strip()

        if user_input.lower() == russian_word.lower():
            print("✅ Правильно!")
            print(f"Английское слово: {english_word}")
        else:
            print(f"❌ Неверно. Правильный ответ: {russian_word}")
            print(f"Английский вариант: {english_word}")

        play_again = input("\nХотите сыграть ещё раз? (да/нет): ").lower()
        if play_again not in ['да', 'д', 'y', 'yes']:
            print("\nСпасибо за игру! До свидания!")
            break


if __name__ == "__main__":
    word_game()