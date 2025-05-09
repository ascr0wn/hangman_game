import random
import streamlit as st
from colorama import Fore, Back, Style
import hangman_words
import hangman_art

# Initialize session state variables
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'chosen_word' not in st.session_state:
    st.session_state.chosen_word = ""
if 'word_length' not in st.session_state:
    st.session_state.word_length = 0
if 'lives_left' not in st.session_state:
    st.session_state.lives_left = 6
if 'guessed_word' not in st.session_state:
    st.session_state.guessed_word = []
if 'word_guessed' not in st.session_state:
    st.session_state.word_guessed = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'message_color' not in st.session_state:
    st.session_state.message_color = ""
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = set()

# Function to start a new game
def start_new_game():
    st.session_state.game_started = True
    st.session_state.chosen_word = random.choice(hangman_words.word_list)
    st.session_state.word_length = len(st.session_state.chosen_word)
    st.session_state.lives_left = 6
    st.session_state.guessed_word = ['_'] * st.session_state.word_length
    st.session_state.word_guessed = False
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.message_color = ""
    st.session_state.guessed_letters = set()

# Function to process a guess
def process_guess(guess):
    if not guess or len(guess) == 0:
        return

    guess = guess.lower()[0]

    # Check if letter was already guessed
    if guess in st.session_state.guessed_letters:
        st.session_state.message = f"You already guessed {guess}. Try a different Letter."
        st.session_state.message_color = "yellow"
        return

    st.session_state.guessed_letters.add(guess)

    guessed_right = False
    count = 0

    for char in st.session_state.chosen_word:
        if char == guess:
            guessed_right = True
            st.session_state.guessed_word[count] = char
        count += 1

    # Check if word is guessed
    guessed_word_string = ''.join(st.session_state.guessed_word)
    if guessed_word_string == st.session_state.chosen_word:
        st.session_state.word_guessed = True
        st.session_state.game_over = True
        st.session_state.message = "You won! Congratulations."
        st.session_state.message_color = "green"
        return

    # If guess was wrong, reduce lives
    if not guessed_right:
        st.session_state.lives_left -= 1
        st.session_state.message = "You Guessed Wrong! Life Deducted"
        st.session_state.message_color = "red"

        # Check if game is over
        if st.session_state.lives_left == 0:
            st.session_state.game_over = True
            st.session_state.message = f"All lives Used. You Lost! Better luck next time. The word was: {st.session_state.chosen_word}"
            st.session_state.message_color = "red"
    else:
        st.session_state.message = f"You correctly guessed the letter '{guess}'!"
        st.session_state.message_color = "green"

# Streamlit UI
st.title("Hangman Game")
st.text(hangman_art.logo)
st.write("Welcome to the Hangman Game")

# Start game button
if not st.session_state.game_started:
    if st.button("Start Game"):
        start_new_game()
    st.stop()

# Display game state
if st.session_state.game_started:
    # Display lives left
    st.write(f"Lives Left: {st.session_state.lives_left}")

    # Display hangman art
    st.text(hangman_art.stages[st.session_state.lives_left])

    # Display current progress
    st.write(f"Your Progress: {' '.join(st.session_state.guessed_word)}")

    # Display message if any
    if st.session_state.message:
        if st.session_state.message_color == "red":
            st.error(st.session_state.message)
        elif st.session_state.message_color == "green":
            st.success(st.session_state.message)
        elif st.session_state.message_color == "yellow":
            st.warning(st.session_state.message)
        else:
            st.info(st.session_state.message)

    # Game over state
    if st.session_state.game_over:
        if st.button("Play Again"):
            start_new_game()
    else:
        # Input for guessing
        guess = st.text_input("Guess a Letter:", key="guess_input", max_chars=1)
        submit_button = st.button("Submit")

        if submit_button and guess:
            process_guess(guess)
            st.rerun()
