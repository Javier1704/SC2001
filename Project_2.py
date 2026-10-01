import random
import time
import matplotlib.pyplot as plt

INF = float("inf")

def relax_matrix(u, v, graph, dist, parent):
    if dist[v] > dist[u] + graph[u][v]:
        dist[v] = dist[u] + graph[u][v]
        parent[v] = u

def extract_min_array(Q, dist):
    min_vertex = Q[0]

    for vertex in Q[1:]:
        if dist[vertex] < dist[min_vertex]:
            min_vertex = vertex

    Q.remove(min_vertex)

    return min_vertex

def dijkstra_matrix(graph, source):
    V = len(graph)
    dist = [INF] * V
    parent = [None] * V
    visited = [False] * V

    dist[source] = 0

    Q = list(range(V))

    while Q:
        u = extract_min_array(Q, dist)

        if dist[u] == INF:
            break

        visited[u] = True

        for v in range(V):
            if graph[u][v] != INF and not visited[v]:
                relax_matrix(u, v, graph, dist, parent)

    return dist, parent

def relax_list(u, v, weight, dist, parent):
    if dist[v] > dist[u] + weight:
        dist[v] = dist[u] + weight
        parent[v] = u
        return True

    return False

def swap(heap, pos, i, j):
    vertex_i = heap[i]
    vertex_j = heap[j]

    heap[i], heap[j] = heap[j], heap[i]

    pos[vertex_i] = j
    pos[vertex_j] = i

def heapify_up(heap, pos, dist, i):
    while i > 0:
        parent_index = (i - 1) // 2
        if dist[heap[parent_index]] <= dist[heap[i]]:
            break

        swap(heap, pos, i, parent_index)
        i = parent_index

def heapify_down(heap, pos, dist, i):
    size = len(heap)

    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        smallest = i

        if left < size:
            if dist[heap[left]] < dist[heap[smallest]]:
                smallest = left

        if right < size:
            if dist[heap[right]] < dist[heap[smallest]]:
                smallest = right

        if smallest == i:
            break

        swap(heap, pos, i, smallest)

        i = smallest

def extract_min_heap(heap, pos, dist):
    min_vertex = heap[0]
    last_vertex = heap.pop()

    if len(heap) > 0:
        heap[0] = last_vertex
        pos[last_vertex] = 0
        heapify_down(heap, pos, dist, 0)

    pos[min_vertex] = -1

    return min_vertex

def dijkstra_heap(graph, source):
    V = len(graph)
    dist = [INF] * V
    parent = [None] * V

    dist[source] = 0

    heap = list(range(V))
    pos = list(range(V))

    heapify_up(heap, pos, dist, pos[source])

    while heap:
        u = extract_min_heap(heap, pos, dist)

        if dist[u] == INF:
            break

        for v, weight in graph[u]:
            if pos[v] != -1:
                changed = relax_list(u, v, weight, dist, parent)

                if changed:
                    heapify_up(heap, pos, dist, pos[v])

    return dist, parent

def generate_graph(V, E):
    matrix = [[INF for _ in range(V)] for _ in range(V)]
    adj_list = [[] for _ in range(V)]

    for i in range(V):
        matrix[i][i] = 0

    edges = set()

    for u in range(V - 1):
        v = u + 1
        weight = random.randint(1, 10)

        matrix[u][v] = weight
        adj_list[u].append((v, weight))

        edges.add((u, v))

    while len(edges) < E:
        u = random.randrange(V)
        v = random.randrange(V)

        if u != v and (u, v) not in edges:
            weight = random.randint(1, 10)

            edges.add((u, v))

            matrix[u][v] = weight
            adj_list[u].append((v, weight))

    return matrix, adj_list

def measure_time(function, graph, source=0, repetitions=5):
    total = 0

    for _ in range(repetitions):
        start = time.perf_counter()

        function(graph, source)

        end = time.perf_counter()

        total += end - start

    return total / repetitions

def run_experiment():
    V_values = [100, 200, 400, 800, 1200]

    matrix_times = []
    heap_times = []

    for V in V_values:
        E = 4 * V

        print("Testing V =", V, "E =", E)

        matrix, adj_list = generate_graph(V, E)

        time_matrix = measure_time(
            dijkstra_matrix,
            matrix,
            repetitions=5
        )

        time_heap = measure_time(
            dijkstra_heap,
            adj_list,
            repetitions=5
        )

        matrix_times.append(time_matrix)
        heap_times.append(time_heap)

        print("Matrix:", time_matrix)
        print("Heap:", time_heap)
        print()

    plt.figure()

    plt.plot(
        V_values,
        matrix_times,
        marker="o",
        label="Adjacency Matrix + Array"
    )

    plt.plot(
        V_values,
        heap_times,
        marker="o",
        label="Adjacency List + Min Heap"
    )

    plt.xlabel("Number of Vertices |V|")
    plt.ylabel("Average Running Time (seconds)")
    plt.title("Dijkstra Algorithm: Empirical Running Time")

    plt.legend()
    plt.grid()

    plt.show()

if __name__ == "__main__":
    run_experiment()