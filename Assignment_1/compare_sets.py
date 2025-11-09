def compare_sets (set1, set2):

    set_1 = set(set1)
    set_2 = set(set2)
    # insure that the sets are sets
    union = set_1.union(set_2)
    # calculate the union between the two sets

    intersection = set_1.intersection(set_2)

    #intersection of two sets 

    if len(union):
        return 1.0
    #If empty sets, then return 1 directly instead of dividing by 0

    jaccard_similairity = len(intersection)/len(union)

    return jaccard_similairity