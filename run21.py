#!/usr/bin/python3
import heapq

# Вирус!
# Здравствуйте, я молдавский вирус.
# По причине ужасной бедности моего создателя и
# низкого уровня развития технологий в нашей стране
# я не способен причинить какой-либо вред вашему компьютеру.
# Поэтому очень прошу: сами сотрите какой-нибудь важный для вас файл,
# а потом разошлите меня по почте другим адресатам.
# Заранее благодарен за понимание и сотрудничиство.
# Закрыть
from typing import Dict, List, Tuple, Set
import sys
from collections import deque


def is_gate(node: str) -> bool:
    return node.isupper()


def bfs_distances(graph, start):
    """Возвращает словарь расстояний от start до всех достижимых узлов."""
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def find_next_virus_position(graph, virus_pos):
    """Возвращает следующую позицию вируса согласно правилам."""
    dist_from_virus = bfs_distances(graph, virus_pos)

    # Собираем все шлюзы и их расстояния
    gate_distances = {}
    for node, d in dist_from_virus.items():
        if is_gate(node):
            gate_distances[node] = d

    if not gate_distances:
        return None  # Вирус изолирован

    min_dist = min(gate_distances.values())
    # Выбираем лексикографически наименьший шлюз с минимальным расстоянием
    target_gate = min(gate for gate, d in gate_distances.items() if d == min_dist)

    # Получаем расстояния от целевого шлюза ко всем узлам
    dist_from_gate = bfs_distances(graph, target_gate)

    # Соседи текущей позиции, лежащие на кратчайшем пути к target_gate
    candidates = []
    for neighbor in graph[virus_pos]:
        # Проверяем: лежит ли neighbor на кратчайшем пути?
        if (neighbor in dist_from_virus and
                neighbor in dist_from_gate and
                dist_from_virus[neighbor] == dist_from_virus[virus_pos] + 1 and
                dist_from_gate[neighbor] == min_dist - 1):
            candidates.append(neighbor)

    if not candidates:
        # Fallback: просто выбираем любого соседа, ведущего к шлюзам (редкий случай)
        for neighbor in sorted(graph[virus_pos]):
            # Проверим, есть ли путь от neighbor до любого шлюза
            dist_nb = bfs_distances(graph, neighbor)
            if any(is_gate(n) for n in dist_nb):
                return neighbor
        # Если совсем нет — выбираем лексикографически наименьшего соседа
        return min(graph[virus_pos])

    return min(candidates)  # лексикографически наименьший


class Graph:
    def __init__(self):
        self.nodes: Dict[str, Set[str]] = {}

    def show_nodes(self):
        return self.nodes

    def add_vertex(self, vertex: str):
        if vertex not in self.nodes:
            self.nodes[vertex] = set()

    def add_edge(self, edge: Tuple[str, str]):
        if edge[0] in self.nodes and edge[1] in self.nodes:
            self.nodes[edge[0]].add(edge[1])
            self.nodes[edge[1]].add(edge[0])

    def pop_edge(self, edge: str, gate: str):
        if edge not in self.nodes:
            return
        self.nodes[edge].remove(gate)


def choose_virus_path(adj: Dict[str, Set[str]], start: str) -> List[str]:

    visited = set()
    queue = list()
    path = list()
    heapq.heappush(queue, (ord(start), start))

    while len(queue) != 0:

        _, node = heapq.heappop(queue)
        visited.add(node)

        if node.isupper():
            path.append(node)
            return path

        neighbors = adj.get(node, [])
        if len(neighbors) != 0:
            path.append(node)
        for neighbor in neighbors:
            if neighbor not in visited:
                heapq.heappush(queue, (ord(neighbor), neighbor))
    return []

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = Graph()
    result = []

    for edge in edges:
        for e in edge:
            graph.add_vertex(e)
            graph.add_edge(edge)

    start = 'a'
    isolated = False

    while not isolated:
        planned_path = choose_virus_path(graph.show_nodes(), start)
        isolated = len(planned_path) == 0
        if not isolated:
            graph.pop_edge(planned_path[-2], planned_path[-1])
            result.append(planned_path[-2:][::-1])
        actual_path = choose_virus_path(graph.show_nodes(), start)
        isolated = len(actual_path) == 0

        if not isolated:
            start = actual_path[1]


    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """


    return result

def main():

    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        edge = '-'.join(edge)
        print(edge)


if __name__ == "__main__":
    main()
