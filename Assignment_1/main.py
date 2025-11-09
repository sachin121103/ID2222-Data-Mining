import shingling
import min_hashing
import compare_sets
import compare_signatures


articles = {
    "text_1": "the cat sat on the mat",
    "text_2": "the cat sat on the mat", 
    "text_3": "the cat sat on the rug",
    "text_4": "the dog ran to me",
    "text_5": "Completely unrelated sentence"
}

document_shingles = {}

for id, text in articles.items():
    shingles = shingling.shingler(text, k=5)
    document_shingles[id] = min_hashing.shingle_hasher(shingles)
    

a_list, b_list = min_hashing.value_gen(100)

signatures = {}

for id, hashed_set in document_shingles.items():
    signatures[id] = min_hashing.minhash(hashed_set, a_list, b_list, num_hashes=100)

document_ids = list(signatures.keys())

for i in range(len(document_ids)):
    for j in range(i+1, len(document_ids)):
        doc1, doc2 = document_ids[i], document_ids[j]

        actual_similarity = compare_sets.compare_sets(document_shingles[doc1], document_shingles[doc2])
        estimated_similarity = compare_signatures.getSimilarity(signatures[doc1], signatures[doc2])

        print(f"{doc1} vs {doc2}")
        print(f"  Actual: {actual_similarity:.3f}")
        print(f"  Estimated: {estimated_similarity:.3f}")
        print(f"  Error: {abs(actual_similarity - estimated_similarity):.3f}")
