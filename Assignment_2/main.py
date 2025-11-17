import data_parser
import apriori_algorithm
import generate_rules
import time
import matplotlib.pyplot as plt

def main():
    # --- 1. Configuration ---
    DATA_FILE = 'T10I4D100K.dat'
    MIN_SUPPORT_PCT = 0.01  # 1% Support
    
    # --- 2. Load Data ---
    print(f"Loading data from {DATA_FILE}...")
    # Note: Ensure data_parser returns a list of sets
    transactions = data_parser.data_parser(DATA_FILE)
    
    num_transactions = len(transactions)
    # Calculate absolute support count (s)
    support_count = MIN_SUPPORT_PCT * num_transactions
    
    print(f"Loaded {num_transactions} transactions.")
    print(f"Support Threshold: {MIN_SUPPORT_PCT*100}% (count >= {support_count})")

    # --- 3. Run Apriori Algorithm ---
    # We need a master dictionary to store {frozenset: count} for ALL itemsets found
    all_frequent_itemsets = {}

    # Step A: Get Frequent Singletons
    print("\n--- Finding Frequent 1-itemsets ---")
    
    # Call your specific singleton function
    current_frequent_itemsets = apriori_algorithm.get_frequent_singletons(transactions, support_count)
    
    if not current_frequent_itemsets:
        print("No frequent items found. Exiting.")
        return

    print(f"Found {len(current_frequent_itemsets)} frequent 1-itemsets.")
    all_frequent_itemsets.update(current_frequent_itemsets)
    
    # Step B: Iterative Loop for k=2, 3, ...
    k = 2
    while True:
        print(f"\n--- Finding Frequent {k}-itemsets ---")
        
        # Call your specific k-itemset function
        # Signature: (previous_k_ton, transaction, support, k)
        next_frequent_itemsets = apriori_algorithm.get_frequent_k_itemsets(
            current_frequent_itemsets, 
            transactions, 
            support_count, 
            k
        )

        if not next_frequent_itemsets:
            print(f"No frequent {k}-itemsets found. Stopping Apriori.")
            break

        print(f"Found {len(next_frequent_itemsets)} frequent {k}-itemsets.")
        
        # Update master list and prepare for next iteration
        all_frequent_itemsets.update(next_frequent_itemsets)
        current_frequent_itemsets = next_frequent_itemsets
        k += 1

    print(f"\nTotal unique frequent itemsets found: {len(all_frequent_itemsets)}")

    # --- 4. Benchmarking Rule Generation ---
    print("\n--- Benchmarking Rule Generation ---")
    
    confidence_levels = [10, 20, 30, 40, 50, 60, 70, 80]
    execution_times = []
    num_rules_found = []
    last_rules_generated = [] # To print examples later

    for conf_pct in confidence_levels:
        min_conf = conf_pct / 100.0
        print(f"Generating rules for {conf_pct}% confidence...", end=" ")
        
        start_time = time.time()
        
        # Run the rule generator
        rules = generate_rules.generate_association_rules(all_frequent_itemsets, min_conf)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        execution_times.append(elapsed)
        num_rules_found.append(len(rules))
        last_rules_generated = rules # Save for example printing
        
        print(f"Done in {elapsed:.4f}s. (Found {len(rules)} rules)")

    # --- 5. Print Example Rules (from the 80% run) ---
    print(f"\nExample Output (Top 5 rules at 80% confidence):")
    if last_rules_generated:
        last_rules_generated.sort(key=lambda x: x[2], reverse=True)
        for ant, cons, conf in last_rules_generated[:5]:
             print(f"{list(ant)} -> {list(cons)} (Conf: {conf:.2f})")
    else:
        print("No rules found at the highest confidence level.")

    # --- 6. Plotting the Graph ---
    plt.figure(figsize=(10, 6))
    
    plt.plot(confidence_levels, execution_times, marker='o', linestyle='-', color='b')
    
    plt.title('Rule Generation Execution Time vs Confidence Level')
    plt.xlabel('Confidence Level (%)')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True)
    plt.xticks(confidence_levels)
    
    # Add labels for number of rules at each point
    for i, txt in enumerate(num_rules_found):
        plt.annotate(f"{txt} Rules", (confidence_levels[i], execution_times[i]), 
                     textcoords="offset points", xytext=(0,10), ha='center')

    print("\nDisplaying graph...")
    plt.show()

if __name__ == "__main__":
    main()