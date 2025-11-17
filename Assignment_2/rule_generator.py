import itertools
from itertools import combinations 
def generate_association_rules(all_frequent_itemsets, min_confidence):
   
    rules = []

    for itemset, union_support_count in all_frequent_itemsets.items(): # input set recieved from apriori
        
        k = len(itemset)
        if k < 2: #only look at doubletons or higher k-tons. cant make an implication from singletons
            continue

        items = list(itemset)

        for i in range(1, k):
            for pair in combinations(items, i): 
                precursor = frozenset(pair) #generate all possible precursons (if part) with the lenght of k - 1
                consequent = itemset - precursor #use set subtraction to find the consequent (then part) 

                if precursor in all_frequent_itemsets:
                    precursor_count = all_frequent_itemsets[precursor] #count the occurences of precursor (if part)
                    
                    confidence = union_support_count / precursor_count#confidence computation

                    if confidence >= min_confidence: 
                        rules.append((precursor, consequent, confidence)) #if passes min then appended to the rules set

    return rules