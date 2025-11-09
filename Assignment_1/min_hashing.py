import random

large_prime = 2**31-1

def shingle_hasher(shingled_set):
    hashed_set = set()
    for s in list(shingled_set):
        hashed_set.add(hash(s) & 0x7FFFFFFF)

    return hashed_set

def value_gen(length):
    a_list = []
    b_list = []
    random.seed(42)
    for _ in range(length):
        a_list.append(random.randint(1, large_prime-1))
        b_list.append(random.randint(0, large_prime-1))
    
    return a_list, b_list


def hash_function(hashed_value, index ,a_list, b_list):
    a = a_list[index]
    b = b_list[index]

    return (a*hashed_value+b) % large_prime

def minhash(hashed_set, a_list, b_list, num_hashes=100):
    signature = []

    for i in range(num_hashes):
        minimum_hash = float('inf')

        for shingle in hashed_set:
            h = hash_function(shingle, i, a_list, b_list)
            minimum_hash = min(minimum_hash, h)

        if minimum_hash != float('inf'):
            signature.append(minimum_hash)
        else:
            signature.append(0)

    return signature