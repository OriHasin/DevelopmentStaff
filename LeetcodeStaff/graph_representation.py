from collections import defaultdict, deque


class DirectedGraph:
    """Graph representation using an adjacency list with a dictionary of lists."""
    def __init__(self):
        self.adj_list = defaultdict(list)  # Efficient adjacency list

    def add_edge(self, src, dest):
        self.adj_list[src].append(dest)

    def print_graph(self):
        """Print adjacency list."""
        for vertex, neighbors in self.adj_list.items():
            print(f"Vertex {vertex}: {' -> '.join(map(str, neighbors))}")






def find_lexicographic_order(words_arr: list) -> list:
    tree = DirectedGraph()

    for word in words_arr:
        for idx in range(len(word)-1):
            tree.add_edge(word[idx], word[idx+1])

    return _topo_sort(tree)



def _topo_sort(tree: DirectedGraph) -> list:
    topo_sort = []
    in_degree = defaultdict(int)

    for node in tree.adj_list:
        for child in tree.adj_list[node]:
            in_degree[child] += 1

    queue = deque([node for node in tree.adj_list if in_degree[node] == 0])

    while queue:
        node = queue.pop()
        topo_sort.append(node)
        # reduce indegree after removing node from tree
        for child in tree.adj_list[node]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.appendleft(child)

    return topo_sort


print(find_lexicographic_order(['abc', 'xyd', 'ax', 'xb']))
