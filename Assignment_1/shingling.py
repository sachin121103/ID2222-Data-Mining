test_1 = "The quick fox, jumped, over the: lazy dog"
test_2 = "Flying fish flew past the space station"
test_3 = "we will not allow you to bring your pet armadillo along"
test_4 = "he figured a few sticks of dynamite were easier than a fishing pole to catch fish"
short_test_1 = "Hello"
short_test_2 = "There"
short_test_3 = "Goodbye"

# This function removes pertinent punctuation from the text
def strip_punctuation(text):
    punctuation =  '.,!?:-;"' + "'"
    cleaned = ''.join(char for char in text if char not in punctuation)
    return cleaned

# This function returns a set of shingles for a given text and k.
def shingler(text, k):
    shingled_set = []
    text = strip_punctuation(text)
    for i in list(range(len(text)-k+1)):
        shingled_set.append(text[i:i+k].lower())

    return set(shingled_set)

# This function creates the 'vocab' by putting every shingle together. This will be a union of all the shingled sets. 

def vocab_builder(*sets):
    return set.union(*sets)



