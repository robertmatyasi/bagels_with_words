from bagels_with_words import BagelsWithWords


def user_interface():

    while True:
        word_length = input("""
        How many letters should the secret word be?\n
        \"RET\" defaults to 5.\n
        """)

        if word_length == '':  # if user presses 'RET'
            word_length = 5
            break

        try:
            val = int(word_length)
            if val < 1:
                print("Please enter a positive integer")
                continue
            break
        except ValueError:
            print("Please enter a positive integer")

    bw = BagelsWithWords(int(word_length), 10)  # default is 10 guesses
    bw.run_game()


if __name__ == '__main__':
    user_interface()
