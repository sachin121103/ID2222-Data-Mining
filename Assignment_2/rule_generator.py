import itertools
from itertools import combinations 
def generate_association_rules(all_frequent_itemsets, min_confidence):
   
    rules = []

    for itemset, union_support_count in all_frequent_itemsets.items():
        
        k = len(itemset)
        if k < 2:
            continue

        items = list(itemset)

        for i in range(1, k):
            for pair in combinations(items, i):
                precursor = frozenset(pair)
                consequent = itemset - precursor 

                if precursor in all_frequent_itemsets:
                    precursor_count = all_frequent_itemsets[precursor]
                    
                    confidence = union_support_count / precursor_count

                    if confidence >= min_confidence:
                        rules.append((precursor, consequent, confidence))

    return rules