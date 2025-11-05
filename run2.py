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
    dist_from_virus = bfs_distances(graph, virus_pos)
    gate_distances = {
        node: d for node, d in dist_from_virus.items() if is_gate(node)
    }
    if not gate_distances:
        return None

    min_dist = min(gate_distances.values())
    target_gate = min(gate for gate, d in gate_distances.items() if d == min_dist)

    dist_from_gate = bfs_distances(graph, target_gate)

    candidates = []
    for neighbor in graph[virus_pos]:
        if is_gate(neighbor):
            continue  # вирус ходит только по обычным узлам
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
        # Собираем все активные шлюзовые коридоры
        gate_corridors = defaultdict(list)
        all_candidates = []
        for node in list(graph.keys()):
            if is_gate(node):
                for nb in list(graph[node]):
                    if not is_gate(nb):
                        gate_corridors[node].append(nb)
                        all_candidates.append((node, nb))

        if not all_candidates:
            break

        # Найдём расстояния от вируса до всех узлов
        dist_virus = bfs_distances(graph, virus_pos)
        gate_distances = {g: dist_virus[g] for g in gate_corridors if g in dist_virus}

        # Найдём критические шлюзы: r > d
        critical_gates = set()
        for gate, corridors in gate_corridors.items():
            if gate in gate_distances:
                d = gate_distances[gate]
                r = len(corridors)
                if r > d:
                    critical_gates.add(gate)

        if critical_gates:
            # Выбираем коридоры только от критических шлюзов
            candidates = [(g, n) for g, n in all_candidates if g in critical_gates]
        else:
            # Нет критических — можно выбирать любой
            candidates = all_candidates

        # Сортируем и выбираем лексикографически наименьший
        candidates.sort()
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