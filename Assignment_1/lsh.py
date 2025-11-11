from itertools import combinations

def lsh(signatures, b, r):
 
    # Get the first signature's length to check the b*r constraint
    first_sig = next(iter(signatures.values()))
    num_hashes = len(first_sig)
    
    if b * r != num_hashes:
        raise ValueError(f"Number of hashes ({num_hashes}) must equal b * r ({b} * {r}).")

    # LSH Bucketing
    buckets = {}
    
    for doc_id, sig in signatures.items():
        
        for i in range(b):
            start_index = i * r
            end_index = (i + 1) * r
            band = sig[start_index:end_index]
            
            # We convert the list to a tuple to make it hashable
            # We add 'i' to the tuple so bands are hashed to different
            # buckets even if they have the same values
            band_hash_key = (i, hash(tuple(band)))
            
            if band_hash_key not in buckets:
                buckets[band_hash_key] = set()
            buckets[band_hash_key].add(doc_id)

    
    candidate_pairs = set()
    
    for bucket in buckets.values():
        # If a bucket has 2 or more items, they are candidates
        if len(bucket) > 1:
            for pair in combinations(bucket, 2):
                # We use frozenset to make the pair order-independent
                candidate_pairs.add(frozenset(pair))
                
    return candidate_pairs