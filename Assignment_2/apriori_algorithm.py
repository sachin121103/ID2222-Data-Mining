from collections import Counter
from itertools import combinations

def get_frequent_singletons(data, s):
    all_items = []
    for d in data:
        for item in d:
            all_items.append(item)
    
    item_count = Counter(all_items)
    frequent_singletons = {}
    
    for item, count in item_count.items():
        if count >= s:
            itemset = frozenset({item})
            frequent_singletons[itemset] = count
    
    return frequent_singletons

def get_frequent_k_itemsets(previous_k_ton, transaction, support, k):
    frequent_items = set()
    for itemset in previous_k_ton.keys():
        for item in itemset:
            frequent_items.add(item)
    
    candidate_counts = {}
    
    for t in transaction:
        relevant_items = t & frequent_items
        
        for pair in combinations(relevant_items, k):
            candidate = frozenset(pair)
            
            if candidate in candidate_counts:
                candidate_counts[candidate] += 1
            else:
                candidate_counts[candidate] = 1
    
    frequent_k_tons = {}
    for candidate, count in candidate_counts.items():
        if count >= support:
            frequent_k_tons[candidate] = count
    
    return frequent_k_tons    
