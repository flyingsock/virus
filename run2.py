#!/usr/bin/python3


# Вирус!
# Здравствуйте, я молдавский вирус.
# По причине ужасной бедности моего создателя и
# низкого уровня развития технологий в нашей стране
# я не способен причинить какой-либо вред вашему компьютеру.
# Поэтому очень прошу: сами сотрите какой-нибудь важный для вас файл,
# а потом разошлите меня по почте другим адресатам.
# Заранее благодарен за понимание и сотрудничиство.
# Закрыть

import heapq
from typing import Dict, List, Tuple, Set
import sys
from collections import deque


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
    # Строим граф
    graph: Dict[str, Set[str]] = {}
    for u, v in edges:
        u = u.strip()
        v = v.strip()
        if u not in graph:
            graph[u] = set()
        if v not in graph:
            graph[v] = set()
        graph[u].add(v)
        graph[v].add(u)

    gates = {node for node in graph if node.isupper()}
    virus = 'a'
    result = []

    while True:
        # 1. Найти текущую цель и следующий шаг
        dist_v = {virus: 0}
        q = deque([virus])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_v:
                    dist_v[v] = dist_v[u] + 1
                    q.append(v)

        # Достижимые шлюзы
        reachable_gates = {g: dist_v[g] for g in gates if g in dist_v}
        if not reachable_gates:
            break

        min_d = min(reachable_gates.values())
        target_gate = min(g for g, d in reachable_gates.items() if d == min_d)

        # 2. Отключаем лексикографически наименьший коридор от target_gate
        neighbors = [nb for nb in graph[target_gate] if not nb.isupper()]
        if neighbors:
            neighbors.sort()
            node = neighbors[0]
            result.append(f"{target_gate}-{node}")
            graph[target_gate].discard(node)
            graph[node].discard(target_gate)

        # 3. Делаем один ход вируса
        dist_g = {target_gate: 0}
        q = deque([target_gate])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_g:
                    dist_g[v] = dist_g[u] + 1
                    q.append(v)

        next_v = None
        for nb in graph[virus]:
            if nb.isupper():
                continue
            if dist_g.get(nb, -1) == dist_g.get(virus, -2) - 1:
                if next_v is None or nb < next_v:
                    next_v = nb

        if next_v is None:
            break
        virus = next_v

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
