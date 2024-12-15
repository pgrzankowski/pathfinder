def get_map_array(map_path):
    with open(map_path, "r") as file:
        map_array = []
        for line in file:
            row = []
            for cell in line.rstrip().split(','):
                row.append(int(cell))
            map_array.append(row)
    return map_array
