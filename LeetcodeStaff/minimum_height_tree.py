from collections import defaultdict, deque


def minimum_depth_roots(nodes: int, edges: list[list[int]]) -> list[int]:
    tree = construct_tree(edges)
    min_depth = nodes
    min_roots = []
    for node in range(nodes):
        depth = run_dfs(tree, node)
        print(f'curr depth: {depth} with root {node}')
        if depth < min_depth:
            min_roots = [node]
            min_depth = depth
        elif depth == min_depth:
            min_roots.append(node)

    return min_roots


def construct_tree(edges):
    tree = defaultdict(list)

    for edge in edges:
        tree[edge[0]].append(edge[1])
        tree[edge[1]].append(edge[0])

    return tree


def run_dfs(tree, node, visited=None, depth=0):
    if visited is None:
        visited = set()

    visited.add(node)
    max_depth = depth

    for child in tree[node]:
        if child not in visited:
            child_depth = run_dfs(tree, child, visited, depth + 1)
            max_depth = max(max_depth, child_depth)

    return max_depth




# Using Topological sorting (special for undirected graphs) to find central nodes == nodes that closest to all
# other graph nodes, which means there longest path will be lowest.
def minimum_depth_roots_optimize(n: int, edges: list[list[int]]) -> list[int]:
    # Edge case for single node
    if n == 1:
        return [0]

    # Step 1: Construct Tree as Adjacency List
    tree = defaultdict(list)
    degree = [0] * n  # Track degree (number of edges) for each node

    for u, v in edges:
        tree[u].append(v)
        tree[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # Step 2: Initialize the queue with leaf nodes (degree == 1)
    queue = deque([i for i in range(n) if degree[i] == 1])

    # Step 3: Topological Sort to Trim Leaves
    remaining_nodes = n
    while remaining_nodes > 2:
        leaves_count = len(queue)
        remaining_nodes -= leaves_count

        # Process all current leaves
        for _ in range(leaves_count):
            leaf = queue.popleft()
            # Remove the leaf from the graph
            for neighbor in tree[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    queue.append(neighbor)

    # Remaining nodes are the roots of Minimum Height Trees
    return list(queue)






print(minimum_depth_roots(4, [[1, 0], [1, 2], [1, 3]]))
print(minimum_depth_roots(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]))
