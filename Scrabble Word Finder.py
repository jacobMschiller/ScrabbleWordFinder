import itertools

def find_legal_words(rack, word_list_file):
    """
    Finds all legal Scrabble words from a given rack, handling blanks.

    Args:
        rack: The player's rack (string), with '?' representing blanks.
        word_list_file: Path to the file containing legal words.

    Returns:
        A set of legal words found.
    """

    legal_words = set()

    with open(word_list_file, 'r') as f:
        word_list = set(line.strip().upper() for line in f)  # More efficient lookup

    # Handle blanks by iterating through possible letter substitutions
    num_blanks = rack.count('?')

    for blank_combos in itertools.product(range(26), repeat=num_blanks): #26 letters in English alphabet
        temp_rack = list(rack)  # Mutable copy
        blank_index = 0
        for i in range(len(temp_rack)):
            if temp_rack[i] == '?':
                temp_rack[i] = chr(ord('A') + blank_combos[blank_index]) #Substitute with A-Z
                blank_index += 1
        
        temp_rack_str = "".join(temp_rack)

        # Generate all possible substrings and permutations
        for i in range(1, len(temp_rack_str) + 1):  # Substring lengths from 1 to rack length
            for substring in itertools.combinations(temp_rack_str, i):
                for permutation in itertools.permutations(substring):
                    word = "".join(permutation)
                    if word in word_list:
                        legal_words.add(word)

    return legal_words

letter_points = {
    " ": 0,
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "K": 5,
    "L": 1,
    "M": 3,
    "N": 1,
    "O": 1,
    "P": 3,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "W": 4,
    "X": 8,
    "Y": 4,
    "Z": 10
    }

def score(word):
    """Returns score of tiles, accounting for bingos"""
    total = 0
    for letter in word:
        total += letter_points[letter]
    if len(word) >= 7:
        return total + 50
    else:
        return total

rack = ""
while not 2 <= len(rack):
    rack = str(input("Give me a rack of at least 2 tiles (use ? as blanks)"))

word_file = r"/Users/USERNAME/Downloads/Scrabble Dictionary.txt"  # Replace with your word list file
found_words = find_legal_words(rack.upper(), word_file)
words_and_scores = []
for word in found_words:
    words_and_scores.append([word, score(word)])
sorted_scores = sorted(words_and_scores, key=lambda x: x[1])
sorted_scores.reverse()
sorted_scores = sorted_scores[:10]

print("Your ten best legal words are:")

for pair in sorted_scores:
    if len(pair[0]) < 7:
        print(pair[0] + " for " + str(pair[1]) + " points")
    else: print(pair[0] + " for " + str(pair[1]) + " points (BINGO!)")
