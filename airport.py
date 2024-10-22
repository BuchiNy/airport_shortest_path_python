from collections import defaultdict

class FlightGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_route(self, airport1, airport2):
        self.graph[airport1].append(airport2)

    def get_graph(self):
        return self.graph


class KosarajuSCC:
    def __init__(self, graph):
        self.graph = graph
        self.transposed_graph = defaultdict(list)
        self.visited = set()
        self.stack = []
        self.sccs = []

    def dfs(self, node):
        self.visited.add(node)
        for neighbor in self.graph[node]:
            if neighbor not in self.visited:
                self.dfs(neighbor)
        self.stack.append(node)

    def transpose(self):
        for node in self.graph:
            for neighbor in self.graph[node]:
                self.transposed_graph[neighbor].append(node)

    def dfs_transpose(self, node, component):
        self.visited.add(node)
        component.append(node)
        for neighbor in self.transposed_graph[node]:
            if neighbor not in self.visited:
                self.dfs_transpose(neighbor, component)

    def find_sccs(self):
        # Perform DFS and store nodes by their finishing times
        for node in list(self.graph.keys()):  # Iterate over a list of keys
            if node not in self.visited:
                self.dfs(node)

        # Transpose the graph
        self.transpose()

        # Perform DFS on the transposed graph in the order of finishing times
        self.visited.clear()
        while self.stack:
            node = self.stack.pop()
            if node not in self.visited:
                component = []
                self.dfs_transpose(node, component)
                self.sccs.append(component)

        return self.sccs


class CompressedGraph:
    def __init__(self, sccs, original_graph):
        self.sccs = sccs
        self.original_graph = original_graph
        self.scc_map = {}
        self.compressed_graph = defaultdict(set)
        self.in_degree = []

    def build_scc_map(self):
        for i, component in enumerate(self.sccs):
            for node in component:
                self.scc_map[node] = i

    def build_compressed_graph(self):
        self.build_scc_map()
        num_sccs = len(self.sccs)
        self.in_degree = [0] * num_sccs

        for node in self.original_graph:
            for neighbor in self.original_graph[node]:
                if self.scc_map[node] != self.scc_map[neighbor]:
                    if self.scc_map[neighbor] not in self.compressed_graph[self.scc_map[node]]:
                        self.compressed_graph[self.scc_map[node]].add(self.scc_map[neighbor])
                        self.in_degree[self.scc_map[neighbor]] += 1

    def get_zero_in_degree_count(self):
        return sum(1 for deg in self.in_degree if deg == 0)



class FlightRouteOptimizer:
    def __init__(self):
        self.flight_graph = FlightGraph()

    def add_flight_routes(self, routes):
        
        for route in routes:
            self.flight_graph.add_route(route[0], route[1])

    def calculate_minimum_routes(self):
        
        # Find SCCs
        scc_finder = KosarajuSCC(self.flight_graph.get_graph())
        sccs = scc_finder.find_sccs()

        # compressed graph and calculate in-degrees
        compressed_graph = CompressedGraph(sccs, self.flight_graph.get_graph())
        compressed_graph.build_compressed_graph()

        # Count the number of SCCs with in-degree 0
        zero_in_degree_count = compressed_graph.get_zero_in_degree_count()

        return zero_in_degree_count

if __name__ == "__main__":
 
    optimizer = FlightRouteOptimizer()

    routes = [
        ('DSM', 'ORD'),
        ('ORD', 'BGI'),
        ('BGI', 'LGA'),
        ('JFK', 'LGA'),
        ('HND', 'JFK'),
        ('HND', 'ICN'),
        ('ICN', 'JFK'),
        ('EWR', 'HND'),
        ('TLV', 'DEL'),
        ('DEL', 'DOH'),
        ('DEL', 'CDG'),
        ('CDG', 'BUD'),
        ('CDG', 'SIN'),
        ('SIN', 'CDG'),
        ('SAN', 'EYW'),
        ('EYW', 'LHR'),
        ('LHR', 'SFO'),
        ('SFO', 'SAN'),
        ('SFO', 'DSM')
    ]

    optimizer.add_flight_routes(routes)

    # Calculate the minimum number of additional routes needed
    result = optimizer.calculate_minimum_routes()
    print(f"minimum number of routes to be added: {result}")
