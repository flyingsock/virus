import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    # Убираем пробелы
    edges = [(u.strip(), v.strip()) for u, v in edges]

    # Строим граф
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    # Находим все шлюзы
    gates = {node for node in graph if node.isupper()}
    virus = 'a'
    result = []

    while True:
        # === Шаг 1: найти текущую цель вируса ===
        # BFS от вируса
        dist_from_virus = {virus: 0}
        queue = deque([virus])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist_from_virus:
                    dist_from_virus[v] = dist_from_virus[u] + 1
                    queue.append(v)

        # Достижимые шлюзы
        reachable_gates = {}
        for gate in gates:
            if gate in dist_from_virus:
                reachable_gates[gate] = dist_from_virus[gate]

        if not reachable_gates:
            break  # вирус изолирован

        # Ближайшие шлюзы
        min_dist = min(reachable_gates.values())
        closest_gates = [g for g, d in reachable_gates.items() if d == min_dist]
        target_gate = min(closest_gates)  # лексикографически наименьший

        # === Шаг 2: отключить лексикографически наименьший коридор от target_gate ===
        neighbors = []
        for nb in graph[target_gate]:
            if not nb.isupper():  # только обычные узлы
                neighbors.append(nb)

        if not neighbors:
            # Шлюз уже отключён — двигаем вирус и продолжаем
            pass
        else:
            neighbors.sort()
            node = neighbors[0]
            result.append(f"{target_gate}-{node}")
            # Отключаем коридор
            graph[target_gate].discard(node)
            graph[node].discard(target_gate)

        # === Шаг 3: вирус делает ход ===
        # BFS от target_gate (в обновлённом графе)
        dist_from_gate = {target_gate: 0}
        queue = deque([target_gate])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist_from_gate:
                    dist_from_gate[v] = dist_from_gate[u] + 1
                    queue.append(v)

        # Находим соседей вируса, ведущих к target_gate
        next_candidates = []
        current_dist = dist_from_gate.get(virus, float('inf'))
        for nb in graph[virus]:
            if nb.isupper():
                continue  # вирус не ходит в шлюзы
            if dist_from_gate.get(nb, float('inf')) == current_dist - 1:
                next_candidates.append(nb)

        if not next_candidates:
            break
        next_virus = min(next_candidates)
        virus = next_virus

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