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



