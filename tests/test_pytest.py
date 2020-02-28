import pytest
from game import random_new_word, WORD_LIST, MAX_FAIL_ATTEMPTS, \
                 Game, Result, ValidationError

def test_random_new_word():
    random_word = random_new_word(WORD_LIST)
    assert random_word in WORD_LIST

def test_create_game():
    game = Game()
    assert game.guessed_word in WORD_LIST
    assert game.hidden_word == '_' * len(game.guessed_word)
    assert game.guess_count == 0
    assert game.called_letters == []

def test_guess_many_letter():
    game = Game()
    with pytest.raises(ValidationError):
        game.guess_letter("abc")

def test_guess_upper_latin_letter():
    game = Game()
    with pytest.raises(ValidationError):
        game.guess_letter("A")

def test_guess_not_latin_letter():
    game = Game()
    with pytest.raises(ValidationError):
        game.guess_letter("1")

def test_guess_called_letter():
    game = Game()
    game.called_letters.append("s")
    with pytest.raises(ValidationError):
        game.guess_letter("s")

def test_guess_letter_success():
    game = Game()
    guessed_word = game.guessed_word
    result = game.guess_letter(guessed_word[0])
    assert result
    assert game.guess_count == 0 
    assert guessed_word[0] in game.called_letters
    assert game.change_hidden_word().startswith(guessed_word[0])

def test_guess_letter_fail():
    game = Game()
    result = game.guess_letter('z')
    assert not result
    assert game.guess_count == 1
    assert 'z' in game.called_letters
    assert game.change_hidden_word() == '_' * len(game.guessed_word)

@pytest.mark.parametrize("attempts_number", [MAX_FAIL_ATTEMPTS, MAX_FAIL_ATTEMPTS+1])
def test_get_result_fail(attempts_number):
    game = Game()
    game.guess_count = attempts_number 
    assert game.get_game_result() == Result.FAIL

@pytest.mark.parametrize("attempts_number", [0, MAX_FAIL_ATTEMPTS - 1])
def test_get_result_continue(attempts_number):
    game = Game()
    game.guess_count = attempts_number 
    assert game.get_game_result() == Result.CONTINUE

@pytest.mark.parametrize("attempts_number", [0, MAX_FAIL_ATTEMPTS - 1])
def test_get_result_win(attempts_number):
    game = Game()
    game.guess_count = attempts_number 
    guessed_word = game.guessed_word
    game.called_letters = list(guessed_word)
    assert game.get_game_result() == Result.WIN
