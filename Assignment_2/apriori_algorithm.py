import itertools
import math 

def first_pass_pruning(dataset, min_support):
   
    item_counts = {} 
    min_support_value = len(dataset) * min_support
    # Pass 1: Count support for each individual item
    for transaction in dataset:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    l1 = set()
    # Prune: Keep only items that meet the minimum support
    for item, count in item_counts.items():
        if count >= min_support_value:
            # Add the item as a frozenset (a 1-itemset) to our L1 set
            l1.add(frozenset([item]))
            
    return l1


def prune_candidates(dataset, candidate_sets, min_support):

    itemset_counts = {}
    min_support_value = len(dataset) * min_support
    # Convert dataset to a list of sets for efficient subset checking
    dataset_sets = [set(transaction) for transaction in dataset]

    for transaction_set in dataset_sets:
        for candidate in candidate_sets:
            # Check if the candidate (a frozenset) is a subset of the transaction
            if candidate.issubset(transaction_set):
                itemset_counts[candidate] = itemset_counts.get(candidate, 0) + 1
    
    lk = set()
    for itemset, count in itemset_counts.items():
        if count >= min_support_value:
            lk.add(itemset)
            
    return lk


def generate_candidates(lk, k):

    ck_plus_1 = set()
    
    # 1. Join Step
    for itemset1 in lk:
        for itemset2 in lk:
            if itemset1 != itemset2:
                # Join two k-itemsets if their union is of size k+1
                union_set = itemset1.union(itemset2)
                
                if len(union_set) == k + 1:
                    # 2. Prune Step (Apriori Property)
                    # Check if all k-subsets of this candidate are also in Lk.
                    has_infrequent_subset = False
                    
                    # Get all subsets of size k
                    for subset in itertools.combinations(union_set, k):
                        if frozenset(subset) not in lk:
                            has_infrequent_subset = True
                            break # No need to check other subsets
                    
                    if not has_infrequent_subset:
                        ck_plus_1.add(union_set)
                        
    return ck_plus_1