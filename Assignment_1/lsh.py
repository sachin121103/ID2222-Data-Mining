from itertools import combinations

def lsh(signatures, b, r):
 
    # Get the first signature's length to check the b*r constraint
    first_sig = next(iter(signatures.values()))
    num_hashes = len(first_sig)
    
    if b * r != num_hashes:
        raise ValueError(f"Number of hashes ({num_hashes}) must equal b * r ({b} * {r}).")

    # LSH Bucketing
    
    # buckets stores collisions.
    # Key: (band_index, band_hash)
    # Value: set(doc_id_1, doc_id_2, ...)
    buckets = {}
    
    # Iterate and document and its signature
    for doc_id, sig in signatures.items():
        
        # Iterate over each band 
        for i in range(b):
            # 1. Slice the signature to get the current band
            start_index = i * r
            end_index = (i + 1) * r
            band = sig[start_index:end_index]
            
            # 2. Hash the band
            # We convert the list to a tuple to make it hashable
            # We add 'i' to the tuple so bands are hashed to different
            # buckets even if they have the same values (e.g., Band 1's
            # [1,2] is different from Band 2's [1,2]).
            band_hash_key = (i, hash(tuple(band)))
            
            # 3. Add the document ID to the corresponding bucket
            if band_hash_key not in buckets:
                buckets[band_hash_key] = set()
            buckets[band_hash_key].add(doc_id)

    # --- Collect Candidate Pairs ---
    
    # We use a set to store unique pairs
    candidate_pairs = set()
    
    # Iterate over all buckets
    for bucket in buckets.values():
        # If a bucket has 2 or more items, they are candidates
        if len(bucket) > 1:
            # 'combinations' creates all unique pairs from the set
            # e.g., combinations({1, 2, 3}, 2) -> (1,2), (1,3), (2,3)
            for pair in combinations(bucket, 2):
                # We use frozenset to make the pair order-independent
                # (doc1, doc2) is the same as (doc2, doc1)
                candidate_pairs.add(frozenset(pair))
                
    return candidate_pairs