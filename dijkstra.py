""" Simple exercise on Dijkstra algorithm """
from __future__ import unicode_literals, print_function

class Graph():
    def __init__(self, nodes_list, nodes_neigh):
        self.nodes_list = nodes_list
        self.nodes_neigh = nodes_neigh

    def nodes_to_check_next(self, current_node):
        nodes_to_check = []
        for node_name, _ in sorted(self.nodes_neigh[current_node], key=lambda node: node[1]):
            nodes_to_check.append(node_name)
            
        return nodes_to_check
    
    @staticmethod
    def fast_delete_dup_without_reorder(nodes_to_check):
        seen = set()
        seen_add = seen.add
        return [x for x in nodes_to_check if not (x in seen or seen_add(x))]

    @staticmethod
    def _min_cost(neigh_cost, n_neigh_cost):
        if neigh_cost > n_neigh_cost:
            return n_neigh_cost, True
        return neigh_cost, False

    def all_best_paths_from_src(self, src):
        nodes_seen = {}
        # dst is a dict of nodes mapped to a tuple containing its
        # cost to the src and its path from the source
        dst = { src: (0,[src])}

        for n in self.nodes_list:
            if not nodes_seen.get(n): # Still not processed
                nodes_seen[n] = True
                # Unpack of node attributes known till now
                if dst.get(n):
                    n_dist_from_src, n_path_from_src = dst[n]
                else:
                    n_dist_from_src, n_path_from_src = (1000, [])
                # For each neighbor, we unpack its attributes
                for neigh_name, neigh_cost in self.nodes_neigh[n]:
                    if neigh_name != src:
                        if dst.get(neigh_name):                
                            # Unpack of neigh attributes known till now
                            neigh_dist_from_src, _ = dst[neigh_name]
                            neigh_cost, updated = self._min_cost(
                                neigh_dist_from_src, n_dist_from_src + neigh_cost
                            )
                            if updated:
                                neigh_path = n_path_from_src.copy()
                                neigh_path.append(neigh_name)
                                dst[neigh_name] = (neigh_cost, neigh_path)
                        else:
                            neigh_cost = n_dist_from_src + neigh_cost
                            neigh_path = n_path_from_src.copy()
                            neigh_path.append(neigh_name)
                            dst[neigh_name] = (neigh_cost, neigh_path)
                    
        return dst




def main():
    nodes_list = ["A","B","C","D","G","F","E"]
    nodes_neigh = { 
        "A": [("B",2), ("C",3), ("D",1)],
        "B": [("A",2), ("C",1), ("E",3)],
        "C": [("A",3), ("B",1), ("D",2), ("E",2)],
        "D": [("A",1), ("C",2), ("E",7), ("F",7)],
        "E": [("B",3), ("C",2), ("D",7), ("F",2), ("G",1)],
        "F": [("D",7), ("E",2), ("G",4)],
        "G": [("E",1), ("F",4)],
    }
    graph = Graph(nodes_list, nodes_neigh)

    print(graph.all_best_paths_from_src("A"))



if __name__ == '__main__':
    main()