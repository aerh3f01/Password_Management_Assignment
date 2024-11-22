# A random passphrase generator
# using xkcdpass module to generate passphrases
#

import xkcdpass.xkcd_password as xp

class PassphraseGenerator:
    """
    Generate Passphrases
    """

    def __init__(self):
        self.num_words = 4
        self.word_length = 5
        self.separator = '-'

    def generate_passphrase(self):
        """
        Generate a passphrase with the defined requirements.
        """
        wordlist = xp.generate_wordlist(wordfile=xp.locate_wordfile(), min_length=self.word_length)
        return xp.generate_xkcdpassword(wordlist, numwords=self.num_words, delimiter=self.separator)
    