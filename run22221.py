import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """
    # Нормализуем узлы
    clean_edges = []
    for u, v in edges:
        clean_edges.append((u.strip(), v.strip()))
    edges = clean_edges

    from collections import defaultdict, deque
    graph = defaultdict(set)
    gates = set()
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
        if u.isupper():
            gates.add(u)
        if v.isupper():
            gates.add(v)

    virus_pos = 'a'
    result = []

    while True:
        # Собираем коридоры шлюз-узел
        gate_edges = []
        for gate in gates:
            for nb in graph[gate]:
                if not nb.isupper():
                    gate_edges.append((gate, nb))
        if not gate_edges:
            break

        # BFS от вируса — найти расстояния до шлюзов
        dist_from_virus = {virus_pos: 0}
        q = deque([virus_pos])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_from_virus:
                    dist_from_virus[v] = dist_from_virus[u] + 1
                    q.append(v)

        # Достижимые шлюзы
        reachable = {g: dist_from_virus[g] for g in gates if g in dist_from_virus}
        if not reachable:
            break

        min_d = min(reachable.values())
        closest_gates = [g for g, d in reachable.items() if d == min_d]
        target_gate = min(closest_gates)  # лексикографически наименьший — цель

        # BFS от целевого шлюза
        dist_from_gate = {target_gate: 0}
        q = deque([target_gate])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_from_gate:
                    dist_from_gate[v] = dist_from_gate[u] + 1
                    q.append(v)

        # Следующий шаг вируса: только к target_gate
        current_d = dist_from_gate.get(virus_pos, float('inf'))
        next_candidates = []
        for nb in graph[virus_pos]:
            if nb.isupper():
                continue
            if dist_from_gate.get(nb, float('inf')) == current_d - 1:
                next_candidates.append(nb)

        if not next_candidates:
            break
        next_virus = min(next_candidates)

        # Отключаем лексикографически наименьший коридор от target_gate
        cut_candidates = []
        for nb in graph[target_gate]:
            if not nb.isupper():
                cut_candidates.append((target_gate, nb))
        if not cut_candidates:
            virus_pos = next_virus
            continue

        cut_candidates.sort()
        gate, node = cut_candidates[0]
        result.append(f"{gate}-{node}")
        graph[gate].discard(node)
        graph[node].discard(gate)

        virus_pos = next_virus

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