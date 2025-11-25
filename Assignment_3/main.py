import time
from triest import TriestBase  
from matplotlib import pyplot as plt

def test_single_M(filepath, M):
    triest = TriestBase(M)
    edges_read = 0
    start_time = time.time()
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            
            u, v = int(parts[0]), int(parts[1])
            
            if u == v:
                continue
            
            triest.process_edge((u, v))
            edges_read += 1
    
    elapsed = time.time() - start_time
    estimate = triest.get_triangle_estimate()
    ground_truth = 11329473  
    
    error_abs = abs(estimate - ground_truth)
    error_rel = (error_abs / ground_truth) * 100
    
    results = {
        'M': M,
        'edges_read': edges_read,
        'unique_processed': triest.t,
        'sample_size': len(triest.S),
        'tau_sample': triest.tau_global,
        'estimate': estimate,
        'ground_truth': ground_truth,
        'error_abs': error_abs,
        'error_rel': error_rel,
        'time': elapsed,
        'rate': edges_read / elapsed
    }
    
    return results

def M_test_graph(x, y):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title('M Values vs Percentage Accuracy')
    plt.xlabel('Accuracy (%)')
    plt.ylabel('M Value)')
    plt.grid(True)
    plt.xticks(x)

    plt.show()

def print_single_result(results):
    print(f"\n{'='*70}")
    print(f"M = {results['M']:,}")
    print(f"{'='*70}")
    print(f"Edges read:         {results['edges_read']:,}")
    print(f"Unique processed:   {results['unique_processed']:,}")
    print(f"Sample size:        {results['sample_size']:,}")
    print(f"Tau (in sample):    {results['tau_sample']:,}")
    print(f"\nGround truth:       {results['ground_truth']:,} triangles")
    print(f"Estimated:          {results['estimate']:,.0f} triangles")
    print(f"Absolute error:     {results['error_abs']:,.0f}")
    print(f"Relative error:     {results['error_rel']:.2f}%")
    print(f"\nTime:               {results['time']:.2f} seconds")
    print(f"Processing rate:    {results['rate']:,.0f} edges/second")
    print(f"{'='*70}")


def compare_multiple_M(filepath, M_values):
    all_results = []
    all_relative_errors = []
    
    print("\n" + "="*70)
    print("TRIÈST-BASE: Testing Multiple M Values")
    print("Dataset: web-NotreDame")
    print("="*70)
    
    for M in M_values:
        print(f"\n\nTesting M = {M:,}...")
        results = test_single_M(filepath, M)
        print_single_result(results)
        all_results.append(results)
        all_relative_errors.append(results['error_rel'])
    
    
    # Summary insights
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    
    best_accuracy = min(all_results, key=lambda x: x['error_rel'])
    fastest = min(all_results, key=lambda x: x['time'])
    
    print(f"Best accuracy:     M={best_accuracy['M']:,} "
          f"({best_accuracy['error_rel']:.2f}% error)")
    print(f"Fastest:           M={fastest['M']:,} "
          f"({fastest['time']:.2f}s)")
    print(f"Ground truth:      8,910,005 triangles")

    print(all_relative_errors)
    
    return all_results, all_relative_errors


filepath = "web-Stanford.txt"
M_values = [1000, 2000, 5000, 7500, 10000, 20000]
results, individual = compare_multiple_M(filepath, M_values)

M_test_graph(M_values, individual)