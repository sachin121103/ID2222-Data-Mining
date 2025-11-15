import data_parser
from collections import Counter
from itertools import combinations
import time

start = time.time()

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


def get_frequent_doubletons(singleton, data, s):
    frequent_items = set()
    for itemset in singleton.keys():
        item = list(itemset)[0]
        frequent_items.add(item)
    
    candidate_counts = {}
    
    for transaction in data:
        relevant_items = transaction & frequent_items
        
        for pair in combinations(relevant_items, 2):
            candidate = frozenset(pair)
            
            if candidate in candidate_counts:
                candidate_counts[candidate] += 1
            else:
                candidate_counts[candidate] = 1
    
    frequent_doubletons = {}
    for candidate, count in candidate_counts.items():
        if count >= s:
            frequent_doubletons[candidate] = count
    
    return frequent_doubletons


support = 1000
transactions = data_parser.data_parser(data_parser.data_file)
singletons = get_frequent_singletons(transactions, support)
doubletons = get_frequent_doubletons(singletons, transactions, support)
print(len(doubletons))

total = time.time() - start

print(f"Time taken: {total: 2f} seconds")