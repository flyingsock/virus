import sys
from collections import deque, defaultdict

def is_gate(node: str) -> bool:
    return node.isupper()

def bfs_distances(graph, start):
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
    # Находим все шлюзы и расстояния до них
    dist_from_virus = bfs_distances(graph, virus_pos)
    gate_distances = {
        node: d for node, d in dist_from_virus.items() if is_gate(node)
    }
    if not gate_distances:
        return None

    min_dist = min(gate_distances.values())
    target_gate = min(gate for gate, d in gate_distances.items() if d == min_dist)

    # BFS от шлюза, чтобы знать расстояния до него
    dist_from_gate = bfs_distances(graph, target_gate)

    candidates = []
    for neighbor in graph[virus_pos]:
        # Проверяем, лежит ли neighbor на кратчайшем пути к target_gate
        if dist_from_gate.get(neighbor, float('inf')) == min_dist - 1:
            candidates.append(neighbor)

    return min(candidates) if candidates else None

def is_safe_to_cut(graph, virus_pos, gate, node):
    """
    Проверяет, безопасно ли отключить коридор gate-node.
    Безопасно = после отключения вирус НЕ окажется в узле, смежном со шлюзом,
    и вообще не сможет выйти на следующем ходу.
    """
    # Создаём временную копию графа
    temp_graph = defaultdict(set)
    for u, neighbors in graph.items():
        temp_graph[u] = set(neighbors)
    # Отключаем коридор
    if node in temp_graph[gate]:
        temp_graph[gate].discard(node)
        temp_graph[node].discard(gate)
    else:
        return False  # такого коридора уже нет

    # Определяем следующую позицию вируса
    next_pos = find_next_virus_position(temp_graph, virus_pos)
    if next_pos is None:
        return True  # вирус изолирован — безопасно

    # Проверяем: находится ли next_pos рядом со шлюзом?
    for nb in temp_graph[next_pos]:
        if is_gate(nb):
            return False  # на следующем ходу выйдет — НЕБЕЗОПАСНО

    return True


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    virus_pos = 'a'
    result = []

    while True:
        # Найти ближайший шлюз
        dist_from_virus = bfs_distances(graph, virus_pos)
        gate_distances = {n: d for n, d in dist_from_virus.items() if is_gate(n)}
        if not gate_distances:
            break

        min_dist = min(gate_distances.values())
        closest_gates = [g for g, d in gate_distances.items() if d == min_dist]
        target_gate = min(closest_gates)

        # Кандидаты — только коридоры от target_gate
        candidates = []
        for nb in graph[target_gate]:
            if not is_gate(nb):
                candidates.append((target_gate, nb))

        if not candidates:
            # Шлюз уже отключён — переходим к следующему ходу вируса
            next_pos = find_next_virus_position(graph, virus_pos)
            if next_pos is None:
                break
            virus_pos = next_pos
            continue

        # Выбираем лексикографически наименьший коридор от этого шлюза
        candidates.sort(key=lambda x: (x[0], x[1]))
        gate, node = candidates[0]

        result.append(f"{gate}-{node}")
        graph[gate].discard(node)
        graph[node].discard(gate)

        # Ход вируса
        next_pos = find_next_virus_position(graph, virus_pos)
        if next_pos is None:
            break
        virus_pos = next_pos

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
        print(edge)

if __name__ == "__main__":
    main()


# a-b
# b-A
# a-c
# c-B