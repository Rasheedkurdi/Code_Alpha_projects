import random

def hangman_game():
    # Predefined list of words
    word_list = ["PYTHON", "JAVASCRIPT", "PROGRAMMING", "DEVELOPER", "COMPUTER"]
    
    # Select a random word
    secret_word = random.choice(word_list).upper()
    word_length = len(secret_word)
    
    # Game variables
    guessed_letters = []
    incorrect_guesses = 0
    max_incorrect = 6
    word_display = ["_"] * word_length
    
    print("=" * 50)
    print("🎮 WELCOME TO HANGMAN! 🎮")
    print("=" * 50)
    print(f"\nThe word has {word_length} letters.")
    print("You have 6 incorrect guesses allowed.")
    
    # Main game loop
    while incorrect_guesses < max_incorrect and "_" in word_display:
        # Display current progress
        print("\n" + "-" * 50)
        print(f"Word: {' '.join(word_display)}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Incorrect guesses remaining: {max_incorrect - incorrect_guesses}")
        
        # Get player's guess
        guess = input("\nGuess a letter: ").upper()
        
        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Invalid input! Please enter a single letter (A-Z).")
            continue
        
        if guess in guessed_letters:
            print(f"❌ You already guessed '{guess}'. Try a different letter!")
            continue
        
        # Add to guessed letters
        guessed_letters.append(guess)
        
        # Check if guess is in the word
        if guess in secret_word:
            print(f"✅ Good guess! '{guess}' is in the word!")
            # Update the display
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    word_display[i] = guess
        else:
            incorrect_guesses += 1
            print(f"❌ Sorry, '{guess}' is not in the word!")
            
            # Show hangman progress
            print(f"💀 Incorrect guesses: {incorrect_guesses}/{max_incorrect}")
    
    # Game over - check result
    print("\n" + "=" * 50)
    if "_" not in word_display:
        print(f"🎉 CONGRATULATIONS! YOU WON! 🎉")
        print(f"The word was: {secret_word}")
    else:
        print(f"💀 GAME OVER! You ran out of guesses. 💀")
        print(f"The word was: {secret_word}")
    
    print("=" * 50)

def main():
    while True:
        hangman_game()
        # Ask to play again
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again not in ['yes', 'y']:
            print("\nThanks for playing! Goodbye! 👋")
            break
        print("\n" + "🔄 Starting new game... 🔄" + "\n")

# Run the game
if __name__ == "__main__":
    main()