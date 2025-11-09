def getSimilarity(list1, list2):
      
    matches = 0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            matches += 1
    
    similarity = matches / len(list1)
    return similarity