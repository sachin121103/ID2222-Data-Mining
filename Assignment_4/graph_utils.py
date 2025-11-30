def load_edge_list(file):
    edges = []

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            else:
                line = line.split(',')
                node1 = int(line[0])
                node2 = int(line[1])

                if len(line) == 3:
                    weight = float(line[2])
                else:
                    weight = 1.0

                edges.append((node1, node2, weight))

    return edges


def build_adjacency_matrix(edges):
    all_nodes = set()
    unique_edges = set()

    for edge in edges:
        all_nodes.add(edge[0])
        all_nodes.add(edge[1])

        u, v = edge[0], edge[1]
        

    unique_nodes = sorted(list(all_nodes))
    nodes_num = len(unique_nodes)

    print(unique_nodes)

    indexed_nodes = {}

    for i in range(nodes_num):
        indexed_nodes[unique_nodes[i]] = i

    adj_matrix = [([0]*nodes_num) for i in range(nodes_num)]

    for ed in edges:
        i = indexed_nodes[ed[0]]
        j = indexed_nodes[ed[1]]

        adj_matrix[i][j] = ed[2]
        adj_matrix[j][i] = ed[2]

    return adj_matrix, indexed_nodes, unique_nodes

def diagnose_edges(edges):
    print("="*50)
    print("EDGE DIAGNOSTICS")
    print("="*50)
    
    # Check for duplicates
    seen = set()
    duplicates = []
    
    for edge in edges:
        u, v = edge[0], edge[1]
        # Normalize edge (smaller node first)
        normalized = (min(u, v), max(u, v))
        
        if normalized in seen:
            duplicates.append((u, v))
        else:
            seen.add(normalized)
    
    print(f"Total edges in file: {len(edges)}")
    print(f"Unique edges (undirected): {len(seen)}")
    print(f"Duplicate edges found: {len(duplicates)}")
    
    if len(duplicates) > 0:
        print("\nFirst 10 duplicates:")
        for i, dup in enumerate(duplicates[:10]):
            print(f"  {dup}")
    
    # Check if edge (1,2) appears in both directions
    has_1_2 = any(e[0] == 1 and e[1] == 2 for e in edges)
    has_2_1 = any(e[0] == 2 and e[1] == 1 for e in edges)
    
    print(f"\nEdge (1,2) exists: {has_1_2}")
    print(f"Edge (2,1) exists: {has_2_1}")
    
    if has_1_2 and has_2_1:
        print("⚠ File contains edges in BOTH directions!")
    
    return len(seen)

# Test it
edges = load_edge_list('example1.dat')
unique_count = diagnose_edges(edges)