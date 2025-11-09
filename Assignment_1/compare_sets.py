def compare_sets(set1, set2):

    set_1 = set(set1)
    set_2 = set(set2)
    union = set_1.union(set_2)
    intersection = set_1.intersection(set_2)

    if len(union) == 0:
        return 0.0

    jaccard_similarity = len(intersection)/len(union)

    return jaccard_similarity