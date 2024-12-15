path = "/home/stpaulo/PycharmProjects/pathfinder/maps/"

with open(path + "one_wall_map.csv", "w") as file:
    for row in range(72):
        line = ""
        for col in range(108):
            if row > 35 and col == 59:
                line += "1,"
            else:
                line += "0,"
        line = line.rstrip(',')
        line += "\n"
        file.write(line)
