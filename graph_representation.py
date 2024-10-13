class Node:
    """Class to represent a node in the linked list."""
    def __init__(self, vertex):
        self.vertex = vertex
        self.next = None

class Graph:
    """Class to represent the graph using an adjacency list."""
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_list = [None] * num_vertices  # Create an array of linked lists

    def add_edge(self, src, dest):
        """Add an edge to the undirected graph."""
        # Add the node to the source's adjacency list
        new_node = Node(dest)
        new_node.next = self.adj_list[src]
        self.adj_list[src] = new_node

        # Since it's an undirected graph, add the node to the destination's adjacency list
        new_node = Node(src)
        new_node.next = self.adj_list[dest]
        self.adj_list[dest] = new_node

    def print_graph(self):
        """Print the adjacency list representation of the graph."""
        for i in range(self.num_vertices):
            print(f"Vertex {i}: ", end="")
            current = self.adj_list[i]
            while current:
                print(f" -> {current.vertex}", end="")
                current = current.next
            print()

# Example usage
graph = Graph(5)
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(0, 3)
graph.add_edge(1, 4)
graph.add_edge(2, 4)
graph.add_edge(3, 4)

graph.print_graph()
