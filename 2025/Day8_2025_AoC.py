from re import I
import urllib.request
import heapq

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

data = [\
'162,817,812',
'57,618,57',
'906,360,560',
'592,479,940',
'352,342,300',
'466,668,158',
'542,29,236',
'431,825,988',
'739,650,466',
'52,470,668',
'216,146,977',
'819,987,18',
'117,168,530',
'805,96,715',
'346,949,466',
'970,615,88',
'941,993,340',
'862,61,35',
'984,92,344',
'425,690,689']

data = get_data(8)

def euclidean_distance(p1, p2):
    """Calculate Euclidean distance between two 3D points"""
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def make_edges(data):
    edges = []
    n = len(data)

    for ii in range(n):
        for jj in range(ii + 1, n):
            a = data[ii]
            b = data[jj]
            aa = [int(val) for val in a.split(',')]
            bb = [int(val) for val in b.split(',')]
            edges.append((euclidean_distance(aa,bb), ii, jj))
    return edges

class UnionFind:
    def __init__(self):
        # Maps node values to their parent/representative node
        self.parent = {}

    def find(self, node):
        """Finds the representative of the set containing the node."""
        if node not in self.parent:
            # If the node is new, it is its own representative initially
            self.parent[node] = node
            return node
        
        if self.parent[node] == node:
            return node
        
        # Path compression: make the node point directly to the root
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        """Merges the sets that contain node1 and node2."""
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            # Merges the first group into the second
            self.parent[root1] = root2
            return True # Groups were merged
        return False # They were already in the same group

def process_new_values(union_find_instance, new_values):
    """
    Adds a set of new values to the Union-Find structure, linking them all
    if any one of them already exists in an existing group.
    """
    if not new_values:
        return

    # Find the representative for the first value
    first_node = new_values[0]
    first_root = union_find_instance.find(first_node)
    
    # Union all subsequent values with the first one's group
    for i in range(1, len(new_values)):
        next_node = new_values[i]
        union_find_instance.union(first_node, next_node)
        
    # The find() method was implicitly called above, updating the internal structure.

def get_final_groups(union_find_instance):
    """Converts the internal Union-Find structure into a list of grouped sets."""
    groups_map = {}
    for node in union_find_instance.parent:
        root = union_find_instance.find(node)
        if root not in groups_map:
            groups_map[root] = set()
        groups_map[root].add(node)
        
    return list(groups_map.values())

def part1(data):
    edges = make_edges(data)
    heap_edges = edges
    heapq.heapify(heap_edges)
    nodes = UnionFind()

    for _ in range(1000):
        val = heapq.heappop(heap_edges)
        process_new_values(nodes, val[1:])

    output = get_final_groups(nodes)
    sizes = sorted([len(val) for val in output], reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


edges = make_edges(data)
heap_edges = edges
heapq.heapify(heap_edges)
nodes = UnionFind()


val = heapq.heappop(heap_edges)
process_new_values(nodes, val[1:])
output = get_final_groups(nodes)
sizes = sorted([len(val) for val in output], reverse=True)

while sum(sizes) < len(data):
    val = heapq.heappop(heap_edges)
    process_new_values(nodes, val[1:])
    output = get_final_groups(nodes)
    sizes = sorted([len(temp) for temp in output], reverse=True)
#    print(output)
#    print(sizes)
#    print(sum(sizes))
print(int(data[val[1]].split(",")[0]) * int(data[val[2]].split(",")[0]))


