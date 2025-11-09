import numpy 


def getSimilarity(list1, list2):

    array_1 = numpy.asarray(list1)
    array_2 = numpy.asarray(list2)

    similiarity = (array_1 == array_2).mean()

    return similiarity



    