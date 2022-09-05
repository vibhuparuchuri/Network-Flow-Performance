import time
from collections import OrderedDict               

class Graph:

    def __init__(self):
        self._nodes = OrderedDict()
        self._edges = []

    def nodes(self):
        return list(self._nodes.values())

    def edges(self):
        return list(self._edges)

    def add_node(self, name, height = 0, excess = 0):
        if self.has_node(name):
            raise ValueError("Node %s already exists" % name)
        self._nodes[name] = Node(name, height, excess)
        return self._nodes[name]

    def add_edge(self, src, dst, capacity = 0, flow = 0, data = None):
        srcnode, dstnode = self._node_lookup([src, dst])
        if srcnode is None or dstnode is None:
            raise ValueError("No node in this graph")
        edge = Edge(srcnode, dstnode, capacity, flow, data)
        self._edges.append(edge)
        srcnode._add_outgoing_edge(edge)
        dstnode._add_incoming_edge(edge)
        return edge

    def remove_edge(self, edge):
        if not edge in self._edges:
            return
        self._edges.remove(edge)
        if edge.is_directed():
            edge.source()._remove_outgoing_edge(edge)
            edge.destination()._remove_incoming_edge(edge)
        else:
            for node in edge.nodes():
                node._remove_undirected_edge(edge)

    def get_node(self, name):
        return self._nodes.get(name)

    def has_node(self, name):
        return name in self._nodes

    def get_edge(self, n1, n2):
        src, dst = self._node_lookup([n1, n2])
        if src is None or dst is None:
            raise ValueError("No such node in this graph")
        return src.edge_to(dst)

    def has_edge(self, n1, n2):
        return self.get_edge(n1, n2) is not None

    def get_reverse_edge(self, edge):
        return edge.destination().edge_to(edge.source())

    def has_reverse_edge(self, edge):
        return self.get_reverse_edge(edge) is not None
    
    def is_directed(self):
        return all( edge.is_directed() for edge in self._edges )

    def is_undirected(self):
        return all( edge.is_undirected() for edge in self._edges )

    def _node_lookup(self, l):
        res = []
        for obj in l:
            if obj in self.nodes():
                res.append(obj)
            else:
                res.append(self._nodes.get(obj))

        return res if not len(res) == 1 else res[0]

    def __str__(self):
        res = "Nodes:\n"
        for node in self._nodes.values():
            res += str(node)

        res += "Edges:\n"
        for edge in self._edges:
            res += str(edge)

        return res

class Node:

    def __init__(self, name, height = 0, excess = 0):
        self._name = name
        self.height = height
        self.excess = excess
        self._outgoing_edges = OrderedDict()
        self._incoming_edges = OrderedDict()

    def _add_outgoing_edge(self, edge):
        self._outgoing_edges[edge.destination()] = edge

    def _add_incoming_edge(self, edge):
        self._incoming_edges[edge.source()] = edge

    def _remove_outgoing_edge(self, edge):
        del self._outgoing_edges[edge.destination()]

    def _remove_incoming_edge(self, edge):
        del self._incoming_edges[edge.source()]

    def name(self):
        return self._name

    def outgoing_edges(self):
        return list(self._outgoing_edges.values())

    def incoming_edges(self):
        return list(self._incoming_edges.values())

    def edge_to(self, node):
        return self._outgoing_edges.get(node)

    def edge_from(self, node):
        return self._incoming_edges.get(node)

    def has_edge_to(self, node):
        return self.edge_to(node) is not None

    def has_edge_from(self, node):
        return self.edge_from(node) is not None

    def clear(self):
        for key, value in vars(self).items():
            if not key.startswith("_"):
                delattr(self, key)

    def __str__(self):
        res = self._name + "\n"
        for key, value in vars(self).items():
            if not key.startswith("_"):
                res += "    " + str(key) + " : " + str(value) + "\n"

        return res

class Edge:

    def __init__(self, node1, node2, capacity = 0, flow = 0, data = None):
        self._node1 = node1
        self._node2 = node2
        self.capacity = capacity
        self.flow = flow
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)

    def nodes(self):
        return [self._node1, self._node2]

    def source(self):
        return self._node1

    def destination(self):
        return self._node2

    def is_directed(self):
        return True;

    def is_undirected(self):
        return not self.is_directed()

    def clear(self):
        for key, value in vars(self).items():
            if not key.startswith("_"):
                delattr(self, key)

    def __str__(self):
        res = self._node1.name() + " --> " + self._node2.name() + "\n"
        for key, value in vars(self).items():
            if not key.startswith("_"):
                res += "    " + str(key) + " : " + str(value) + "\n"

        return res

# Script for Preflow-push algorithm 

def get_active_node(graph, s, t):
    for node in graph.nodes():
        if not node is t and not node is s and node.excess > 0:
            return node
    return None

def has_active_node(graph, s, t):
    return True if not get_active_node(graph, s, t) is None else False

def push_flow(node):
    push_flow_result = False
    for edge in node.outgoing_edges():
        neighbor = edge.destination()
        if not node.height == neighbor.height + 1 or (edge.flow == edge.capacity):
            continue
        push_flow_result = True
        reverse_edge = node.edge_from(neighbor)

        push = min(edge.capacity - edge.flow, node.excess)
        edge.flow = edge.flow + push
        reverse_edge.flow = reverse_edge.flow - push
        neighbor.excess = neighbor.excess + push
        node.excess = node.excess - push

        if node.excess == 0:
            break

    return push_flow_result

def relabel(node):
    min_height = None
    for edge in node.outgoing_edges():
        if edge.flow == edge.capacity:
            continue
        if min_height == None or edge.destination().height < min_height:
            min_height = edge.destination().height

    node.height = min_height + 1
        
def solve_max_flow(graph, s, t):
    for node in graph.nodes():
        node.height = 0
        node.excess = 0
    
    for edge in graph.edges():
        edge.flow = 0
        if not graph.has_reverse_edge(edge):
            graph.add_edge(edge.destination(), edge.source(), 0, 0, {"tmp" : True})
    
    s.height = len(graph.nodes())
    for edge in s.outgoing_edges():
        edge.flow = edge.capacity
        edge.destination().excess = edge.flow
        edge.destination().edge_to(s).flow = -edge.capacity
    
    print("Solving max flow ------------------")
    while has_active_node(graph, s, t):
        node = get_active_node(graph, s, t)
        if not push_flow(node):
            relabel(node)

    # cleanup
    for edge in graph.edges():
        if hasattr(edge, "tmp"):
            graph.remove_edge(edge)

F1 = "r-e-100.txt"
F2 = "r-e-150.txt"
F3 = "r-e-200.txt"
F4 = "r-e-250.txt"
F5 = "r-e-300.txt"


#enter only filename to ensure cold-starts
input_graphs = [F1,F2,F3,F4,F5]


#Reading input text files to create network flow graphs

for input_graph in input_graphs:
    G = Graph()
    with open(input_graph) as f:
        lines = f.readlines()
    for line in lines:
        row = line.split()
        src_node = row[0]
        dest_node = row[1]
        capacity = int(row[2])
        if not G.get_node(src_node):
            G.add_node(src_node)
        if not G.get_node(dest_node):
            G.add_node(dest_node)
        G.add_edge(src_node, dest_node, capacity)
    print(f'Graph generated for {input_graph}')

    t1 = time.process_time()
    solve_max_flow(G, G.get_node('s'),G.get_node('t'))
    t2 = time.process_time()
    
    print(f'Runtime  {(t2 - t1)} s')
    indegree_edges_to_sink = G.get_node('t').incoming_edges()
    max_flow = 0
    for edge in indegree_edges_to_sink:
        max_flow += edge.flow
    print(f'max flow is {max_flow}')

