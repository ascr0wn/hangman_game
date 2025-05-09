import random
from colorama import Fore, Back, Style
import hangman_words
import hangman_art

print(hangman_art.logo,Style.BRIGHT,Fore.GREEN,"Welcome to the Hangman Game", Style.RESET_ALL, "\nGame Started\nWord Selected\nStart Guessing...")
chosen_word = random.choice(hangman_words.word_list)
wordLength = len(chosen_word)
livesLeft = 6
guessedWord = ['_'] * wordLength
wordGuessed = False

while livesLeft:
    count = 0
    guessedRight = False
    print('\n')
    print(Fore.LIGHTGREEN_EX, f"Lives Left: {livesLeft}", Style.RESET_ALL)
    print(Fore.CYAN, hangman_art.stages[livesLeft], Style.RESET_ALL)
    print(f"Your Progress: {guessedWord}")
    guessedWordInString = ''.join(guessedWord)
    result = guessedWordInString == chosen_word
    if result:
        wordGuessed = True
        break
    guess = input("Guess a Letter: ")[0].lower()
    if guess in guessedWordInString:
        print(Fore.YELLOW, f"You already guessed {guess}. Try a different Letter.", Style.RESET_ALL)
        guessedRight = True
        continue
    for char in chosen_word:
        if char == guess:
            guessedRight = True
            print(Fore.GREEN,f"You correctly guessed the {count} character!",Style.RESET_ALL)
            guessedWord[count] =  char
        count += 1
    if not guessedRight:
        print(Fore.RED, "You Guessed Wrong! Life Deducted", Style.RESET_ALL)
        livesLeft -= 1

if wordGuessed:
    print(Fore.BLACK, Back.GREEN, "You won! Congratulations.", Style.RESET_ALL)
else:
    print(Fore.CYAN, hangman_art.stages[livesLeft], Style.RESET_ALL)
    print(f"The word was: {chosen_word}")
    print(Back.RED, Fore.BLACK,"All lives Used. You Lost! Better luck next time.", Style.RESET_ALL)
