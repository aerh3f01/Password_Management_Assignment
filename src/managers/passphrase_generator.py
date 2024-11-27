# A random passphrase generator using xkcdpass module to generate passphrases

import random
import string
import xkcdpass.xkcd_password as xp


class PassphraseGenerator:
    """
    Generate secure passphrases with additional entropy.
    """
    def __init__(self, num_words=4, word_length=4, separator='-', 
                 min_length=15, min_uppercase=2, min_numbers=2):
        """
        Initialize the passphrase generator with default or user-defined parameters.

        Args:
            num_words (int): Number of words in the passphrase.
            word_length (int): Minimum length of each word in the wordlist.
            separator (str): Separator used between words.
            min_length (int): Minimum length of the final passphrase.
            min_uppercase (int): Minimum number of uppercase letters.
            min_numbers (int): Minimum number of numeric characters.
        """
        self.num_words = num_words
        self.word_length = word_length
        self.separator = separator
        self.min_length = min_length
        self.min_uppercase = min_uppercase
        self.min_numbers = min_numbers

    @staticmethod
    def _insert_random_characters(words, chars, count, transform=None):
        """
        Static utility method to insert random characters into the passphrase.

        Args:
            mypw (str): The initial passphrase.
            chars (str): The set of characters to insert (e.g. digits).
            count (int): Number of characters to insert.
            transform (func): Optional function to apply to characters (e.g. str.upper).

        Returns:
            str: Passphrase with the added characters.
        """
        for _ in range(count):
            word_index = random.randint(0, len(words) - 1)  # Choose a random word
            word = list(words[word_index])  # Convert word to a list of characters
            char_index = random.randint(0, len(word) - 1)  # Choose a random character in the word
            
            if transform:
                word[char_index] = transform(word[char_index])  # Apply transformation (e.g., uppercase)
            else:
                word[char_index] = random.choice(chars)  # Replace with a character from the set
            
            words[word_index] = ''.join(word)  # Update the word in the list
        return words

    def generate_passphrase(self):
        """
        Generate a secure passphrase that meets the defined requirements.
        """
        # Generate the base passphrase
        wordlist = xp.generate_wordlist(wordfile=xp.locate_wordfile(), min_length=self.word_length)
        words = xp.generate_xkcdpassword(wordlist, numwords=self.num_words, delimiter=self.separator).split(self.separator)

        # Ensure the passphrase meets minimum length by adding more words if needed
        while sum(len(word) for word in words) + len(self.separator) * (len(words) - 1) < self.min_length:
            words.append(random.choice(wordlist))

        # Add random characters to the start or end of words
        words = self._insert_random_characters(words, string.ascii_uppercase, self.min_uppercase)
        words = self._insert_random_characters(words, string.digits, self.min_numbers)

        # Rejoin the words with the separator
        return self.separator.join(words)