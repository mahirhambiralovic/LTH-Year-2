import sys
import math
from queue import Queue
import copy

"""
graph is a nested dict where graph[u][v] returns (capacity, flow)
p_list is a list with priority of removals
edge_indices[i] gives edge(u,v) on index i
"""

def main():
    graph, p_list, edge_indices, target, required_capacity = read_input()
    graph_original = copy.deepcopy(graph)
    do_flow(graph, target)
    #printgraph(graph)
    #print(get_max_cap(graph))
    old_max = 0
    for i in range(len(p_list)):
        # TODO Börja med att bygga upp kanter än att ta bort
        u_rem, v_rem = edge_indices[p_list[i]]
        del graph_original[u_rem][v_rem]
        del graph_original[v_rem][u_rem]

        graph = copy.deepcopy(graph_original)
        #print("\nREMOVAL {}: removing ({} {})".format(i, u_rem, v_rem))

        do_flow(graph, target)
        #printgraph(graph)

        max = get_max_cap(graph)
        #print(max)
        if max < required_capacity:
            print(i, old_max)
            break
        old_max = max

def do_flow(graph, target):
    path, delta = bfs(graph, target)
    while delta != 0:
        increase_flow(path, delta, graph, target)
        path, delta = bfs(graph, target)

def get_max_cap(graph):
    max = 0
    for val in graph[0].keys():
        max = max + graph[0][val][1]
    return max

def read_input():
    N, M, C, P = list(map(int,sys.stdin.readline().split()))
    graph = {}
    edge_indices = []
    for i in range(M):
        u, v, c = list(map(int,sys.stdin.readline().split()))
        if u not in graph:
            graph[u] = {}
        if v not in graph:
            graph[v] = {}
        graph[u][v] = (c, 0) # Fill [u][v] with tuple (capacity, flow)
        graph[v][u] = (c, 0) # bidirectional
        edge_indices.append((u,v))

    p_list = []
    for i in range(P):
        p_list.append(list(map(int,sys.stdin.readline().split()))[0])

    return graph, p_list, edge_indices, N-1, C


def increase_flow(path, delta, graph, target):
    v = target
    u = path[v]
    while True:
        #print(u)
        cap, flow = graph[u][v] # increase flow with delta
        graph[u][v] = (cap, flow + delta)

        cap_b, flow_b = graph[v][u]
        graph[v][u] = (flow + delta, flow_b)

        if u == 0:
            break
        v = u
        u = path[v]

    #print(graph)



def bfs(graph, target): #Returns a list of the path and the minimum flow we can increase.
    current_node = 0
    pred = {}

    queue = Queue()
    queue.put(current_node)
    visited = set()
    min_delta = sys.maxsize
    while not queue.empty():
        current_node = queue.get()
        for neighbor in graph[current_node]:
            cap, flow = graph[current_node][neighbor]
            if neighbor not in visited and cap - flow != 0:
                #print("visiting: {}".format(neighbor))
                visited.add(neighbor)
                queue.put(neighbor)
                pred[neighbor] = current_node
                cap, flow = graph[current_node][neighbor]
                delta = cap - flow
                if delta < min_delta:
                    min_delta = delta

                if neighbor == target:
                    return pred, min_delta
    #print("No path")
    return {}, 0

def printgraph(graph):
    for key in graph:
        print("Edges from {}".format(key))
        print(graph[key])

if __name__ == "__main__":
    main()
