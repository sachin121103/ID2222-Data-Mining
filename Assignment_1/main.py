import shingling
import min_hashing
import compare_sets
import compare_signatures
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time


# Start timing
total_start = time.time()

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

# Collect data for analysis
actual_similarities = []
estimated_similarities = []
errors = []

for i in range(len(document_ids)):
    for j in range(i+1, len(document_ids)):
        doc1, doc2 = document_ids[i], document_ids[j]

        actual_similarity = compare_sets.compare_sets(document_shingles[doc1], document_shingles[doc2])
        estimated_similarity = compare_signatures.getSimilarity(signatures[doc1], signatures[doc2])
        error = abs(actual_similarity - estimated_similarity)

        actual_similarities.append(actual_similarity)
        estimated_similarities.append(estimated_similarity)
        errors.append(error)

plt.figure(figsize=(10, 6))
plt.hist(actual_similarities, bins=50, edgecolor='black', alpha=0.7)
plt.xlabel('Jaccard Similarity', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Actual Similarities', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('similarity_distribution.png', dpi=300, bbox_inches='tight')


total_time = time.time() - total_start

# GRAPHS AND STATISTICS


print("STATISTICS")
print(f"Total documents: {len(articles)}")
print(f"Total comparisons: {len(actual_similarities)}")
print(f"Average error: {np.mean(errors):.4f}")
print(f"Max error: {np.max(errors):.4f}")
print(f"Min error: {np.min(errors):.4f}")
print(f"Total execution time: {total_time:.2f}s")
print("-"*80)

# Plot 1: MinHash Accuracy - Actual vs Estimated Similarity
plt.figure(figsize=(10, 6))
plt.scatter(actual_similarities, estimated_similarities, alpha=0.5, s=20)
plt.plot([0, 1], [0, 1], 'r--', label='Perfect Estimation', linewidth=2)
plt.xlabel('Actual Jaccard Similarity', fontsize=12)
plt.ylabel('Estimated Similarity (MinHash)', fontsize=12)
plt.title('MinHash Accuracy: Actual vs. Estimated Similarity', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)
plt.tight_layout()
plt.savefig('minhash_accuracy.png', dpi=300, bbox_inches='tight')
print("Saved: minhash_accuracy.png")

# Plot 2: Distribution of Actual Similarities
plt.figure(figsize=(10, 6))
plt.hist(actual_similarities, bins=50, edgecolor='black', alpha=0.7)
plt.xlabel('Jaccard Similarity', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Actual Similarities', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('similarity_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: similarity_distribution.png")

# Plot 3: Error Distribution
plt.figure(figsize=(10, 6))
plt.hist(errors, bins=50, edgecolor='black', alpha=0.7, color='orange')
plt.xlabel('Absolute Error', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of MinHash Estimation Errors', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('error_distribution.png', dpi=300, bbox_inches='tight')
print("Saved: error_distribution.png")
