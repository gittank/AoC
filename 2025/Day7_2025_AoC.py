import urllib.request
from collections import defaultdict

def gather_input_data(url, sessionId, transform=lambda x: str(x, "utf-8").strip('\n')):
    request = urllib.request.Request(url)
    request.add_header("cookie", "session={}".format(sessionId)) # Source the data directly from AoC

    values = []
    with urllib.request.urlopen(request) as data:
        for line in data:
            values.append(transform(line))

    return values

def get_data(day, year=2025):
    with open('sessionID') as f:
        sessionId = f.readlines()[0]
    url = "https://adventofcode.com/%d/day/%d/input"%(year,day)
    data = gather_input_data(url, sessionId)
    return data

def find_all_indices(main_string, target_element):
    indices = []
    for index, char in enumerate(main_string):
        if char == target_element:
            indices.append(index)
    return indices

def part1(data):
    split = 0
    has_laser = []
    idx = find_all_indices(data[0], 'S')
    has_laser.extend(idx) 
    for row in data[::2]:
        splitter = (find_all_indices(row, '^'))
        for split_idx in splitter:
            if split_idx in has_laser:
                has_laser.extend([split_idx+1, split_idx-1])
                has_laser.remove(split_idx)
                has_laser = list(set(has_laser))
                split += 1
    return split

def part2(data):
    split = 0
    has_laser = []
    idx = find_all_indices(data[0], 'S')
    has_laser.extend(idx) 
    worlds = defaultdict(int)
    worlds[idx[0]] = 1
    for row in data[::2]:
        splitter = (find_all_indices(row, '^'))
        remove_list = []
        for split_idx in splitter:
            if split_idx in has_laser:
                remove_list.append(split_idx)
                has_laser.extend([split_idx+1, split_idx-1])
                has_laser.remove(split_idx)
                has_laser = list(set(has_laser))
                worlds[split_idx-1] = worlds[split_idx] + worlds[split_idx-1]
                worlds[split_idx+1] = worlds[split_idx] + worlds[split_idx+1]
        for ii in remove_list:
            worlds[ii] = 0
    return sum(worlds.values()) 

def main(unit_test):
    if unit_test:
        data = [\
                '.......S.......',
                '...............',
                '.......^.......',
                '...............',
                '......^.^......',
                '...............',
                '.....^.^.^.....',
                '...............',
                '....^.^...^....',
                '...............',
                '...^.^...^.^...',
                '...............',
                '..^...^.....^..',
                '...............',
                '.^.^.^.^.^...^.',
                '...............']
    else:
        data = get_data(7)

    print(part2(data))

    
if __name__ == "__main__":
    main(False) 