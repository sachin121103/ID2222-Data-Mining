from data_parser import data_parser
import apriori_algorithm as apriori 
import math 

def main():
   
    apriori.MIN_SUPPORT = 0.01  
    DATA_FILE = 'T10I4D100K.dat'
    
    #parse data
    print(f"Loading data from {DATA_FILE}...")
    dataset = data_parser(DATA_FILE)
    print(f"Loaded {len(dataset)} transactions.")
    print(f"Using a minimum support threshold of {apriori.MIN_SUPPORT * 100}%\n")

    # --- 3. Start Apriori Algorithm ---
    k = 1
    all_frequent_sets = [] # This will store all Lk sets

    # Get L1 (Frequent 1-itemsets)
    print("--- Running Pass 1 (Finding L1) ---")
    L1 = apriori.first_pass_pruning(dataset)
    
    if not L1:
        print("No frequent 1-itemsets found. Stopping.")
        return
        
    print(f"Found {len(L1)} frequent 1-itemsets (L1)")
    all_frequent_sets.extend(L1)
    
    # Lk will hold the results from the previous pass (L_k)
    Lk = L1

    # --- 4. Iterative Pipeline (k > 1) ---
    while Lk:
        k += 1
        print(f"\n--- Running Pass {k} ---")
        
        # Generate Candidates (Ck)
        print(f"Generating C{k} from L{k-1}...")
        Ck = apriori.generate_candidates(Lk, k - 1)
        
        if not Ck:
            print(f"No more candidates (C{k}) generated. Stopping.")
            break
            
        print(f"Generated {len(Ck)} candidates for C{k}.")

        # Prune Candidates (Lk)
        print(f"Pruning C{k} to find L{k}...")
        Lk = apriori.prune_candidates(dataset, Ck)
        
        if not Lk:
            print(f"No frequent {k}-itemsets (L{k}) found. Stopping.")
            break
            
        print(f"Found {len(Lk)} frequent {k}-itemsets (L{k}).")
        all_frequent_sets.extend(Lk)

    # --- 5. Print Final Results ---
    print("\n--- Apriori Algorithm Complete ---")
    print(f"Found a total of {len(all_frequent_sets)} frequent itemsets:")
    
    # Uncomment the following lines if you want to print every set
    # print("----------------------------------")
    # for itemset in all_frequent_sets:
    #     print(itemset)
    # print("----------------------------------")

# Standard boilerplate to run the main() function
if __name__ == "__main__":
    main()