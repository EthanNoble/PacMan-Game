from typing import Dict, Set, List

class Graph:
    def __init__(self):
        self.adj_list: Dict[int, Set[int]] = {}
        self.new_key: int = 0 # Counter to keep track of the next key to use


    def __str__(self) -> str:
        return_str: str = ''
        for key in self.adj_list:
            return_str += f'{key}: {str(self.adj_list[key])}\n'
        return return_str
    

    def add_node(self) -> None:
        self.adj_list[self.new_key] = set()
        self.new_key += 1

    def remove_node(self, node: int) -> None:
        if node not in self.adj_list:
            raise KeyError(f'Node {node} not found in graph')
        
        # Remove the node from the node's neighbors' neighbors
        for neighbor in self.neighbors_of(node):
            self.adj_list[neighbor].remove(node)

        # Remove the node's neighbors
        self.adj_list[node].clear()

    def add_edge_between(self, node_one: int, node_two: int) -> None:
        if node_one not in self.adj_list:
            raise KeyError(f'Node {node_one} not found in graph')
        if node_two not in self.adj_list:
            raise KeyError(f'Node {node_two} not found in graph')
        
        self.adj_list[node_one].add(node_two)
        self.adj_list[node_two].add(node_one)

    def neighbors_of(self, node: int) -> Set[int]:
        return self.adj_list[node]


    def BFS(self, start_node: int, end_node: int) -> List[int]:
        path: List[int] = []
        distance: Dict[int, float] = {}
        previous: Dict[int, int | None] = {}
        Q: Set[int] = set()

        for vertex in self.adj_list.keys():
            distance[vertex] = float('inf')
            previous[vertex] = None
            Q.add(vertex)

        distance[start_node] = 0

        while len(Q) > 0:
            u = min(Q, key=distance.get)

            # If we have reached the end node, we can stop
            if u == end_node:
                while previous[u] is not None:
                    path.insert(0, u)
                    u = previous[u]
                if len(path) > 0: # If there is indeed a path
                    path.insert(0, start_node) # Add the start node to the path
                break
            else:
                Q.remove(u)

                for v in self.adj_list[u]:
                    alt: float = distance[u] + 1
                    if alt < distance[v]:
                        distance[v] = alt
                        previous[v] = u
        
        return path