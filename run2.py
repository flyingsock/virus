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
    count = 1
    while not isolated:
        planned_path = choose_virus_path(graph.show_nodes(), start)
        isolated = True if len(planned_path) == 0 else False
        if not isolated:
            graph.pop_edge(planned_path[-2], planned_path[-1])
            result.append(planned_path[-2:][::-1])
        actual_path = choose_virus_path(graph.show_nodes(), start)
        isolated = True if len(actual_path) == 0 else False

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

