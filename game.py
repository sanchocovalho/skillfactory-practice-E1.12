import os
import signal
import random
import time
from string import ascii_lowercase, ascii_uppercase
from enum import Enum

class ValidationError(BaseException):
    em = {1101: "Необходимо вводить по одной букве.", \
          1102: "Вы ввели латинскую букву в верхнем регистре.", \
          1103: "Это не латинская буква.", \
          1104: "Эту букву вы уже называли."}

WORD_LIST = ['skillfactory', 'testing', 'blackbox', 'pytest', 'unittest', 'coverage']
MAX_FAIL_ATTEMPTS = 4

class Result(Enum):
    FAIL = 0
    WIN = 1
    CONTINUE = -1

def random_new_word(word_list):
    return random.choice(word_list)

class Game():
    def __init__(self):
        self.guessed_word = random_new_word(WORD_LIST)
        self.hidden_word = '_' * len(self.guessed_word)
        self.guess_count = 0
        self.called_letters = []

    def guess_letter(self, letter):
        if len(letter) != 1:
            raise ValidationError(1101)
        if letter in ascii_uppercase:
            raise ValidationError(1102)
        if letter not in ascii_lowercase:
            raise ValidationError(1103)
        if letter in self.called_letters:
            raise ValidationError(1104)
        self.called_letters.append(letter)
        if letter in self.guessed_word:
            self.hidden_word = self.change_hidden_word()
            return True
        else:
            self.guess_count += 1
            return False

    def change_hidden_word(self):
        current_state = []
        for letter in self.guessed_word:
            if letter in self.called_letters:
                current_state.append(letter)
            else:
                current_state.append('_')
        return ''.join(current_state)

    def get_game_result(self):
        if self.guess_count >= MAX_FAIL_ATTEMPTS:
            return Result.FAIL
        elif self.guessed_word == self.change_hidden_word():
            return Result.WIN
        else:
            return Result.CONTINUE

def make_rus(count):
    count = MAX_FAIL_ATTEMPTS - count
    if count == 0:
        return f'{count} штрафных очков'
    elif count == 1:
        return f'{count} штрафное очко'
    else:
        return f'{count} штрафных очка'

def gameplay():
    game = Game()
    print('-' * 50)
    print('Вам необходимо угадать слово из {} букв.'.format(len(game.guessed_word)))
    print('Слово содержит только латинские буквы в нижнем регистре.')
    print('У вас есть только 4 штрафных очка...')
    print('-' * 50)
    print(game.hidden_word)

    while True:
        letter = str(input())

        try:
            result = game.guess_letter(letter)
            if result is True:
                print('Вы угадали букву!!!')
            else:
                print('Неудачная попытка. У вас {}.'.format(make_rus(game.guess_count)))
        except ValidationError as e:
            print("Ошибка: %s" % e.em[e.args[0]])

        print(game.hidden_word)

        result = game.get_game_result()
        if result == Result.WIN:
            print('Вы выиграли!!!')
            break
        elif result == Result.FAIL:
            print('Вы проиграли!?!')
            break
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    print('-' * 50)
    print('Сочетание клавиш Ctrl+C для выхода...')
    signal.signal(signal.SIGINT, lambda *_: os._exit(1))
    while True:
        gameplay()
