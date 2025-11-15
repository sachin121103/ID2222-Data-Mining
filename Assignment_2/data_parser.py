def data_parser(data_file):
    set_list = []
    with open(data_file, 'r') as df:
        for line in df:
            line = line.strip().split()
            individual_set = set(int(x) for x in line)
            set_list.append(individual_set)

    return set_list


data_file = "T10I4D100K.dat"
