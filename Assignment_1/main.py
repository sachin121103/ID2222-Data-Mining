import shingling
import min_hashing
import compare_sets
import compare_signatures
import pandas as pd
import matplotlib.pyplot as plt


wars = pd.read_csv('data/middle_east_wars.csv', encoding='latin-1')

iraq_wars = wars[wars['Keyword'] == 'Iraq']
articles = iraq_wars['Headlines'].tolist()

document_shingles = {}

for id, text in enumerate(articles):
    shingles = shingling.shingler(text, k=5)
    document_shingles[id] = min_hashing.shingle_hasher(shingles)
    

a_list, b_list = min_hashing.value_gen(100)

signatures = {}

for id, hashed_set in document_shingles.items():
    signatures[id] = min_hashing.minhash(hashed_set, a_list, b_list, num_hashes=100)

document_ids = list(signatures.keys())

actual_similarities = []

for i in range(len(document_ids)):
    for j in range(i+1, len(document_ids)):
        doc1, doc2 = document_ids[i], document_ids[j]
        actual_similarity = compare_sets.compare_sets(document_shingles[doc1], document_shingles[doc2])
        actual_similarities.append(actual_similarity)

plt.hist(actual_similarities, bins=50, edgecolor='black')
plt.xlabel('Jaccard Similarity')
plt.ylabel('Frequency')
plt.title('Distribution of Headline Similarities in the Iraq War')
plt.show()