import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # Убираем пробелы
    edges = [(u.strip(), v.strip()) for u, v in edges]

    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    # Выделяем шлюзы
    gates = {node for node in graph if node.isupper()}
    virus = 'a'
    result = []

    while True:
        # === 1. Найти ближайший шлюз ===
        # BFS от вируса
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

        min_dist = min(reachable_gates.values())
        # Среди шлюзов с min_dist — лексикографически наименьший
        target_gate = min(g for g, d in reachable_gates.items() if d == min_dist)

        # === 2. Найти следующий шаг вируса ===
        # BFS от целевого шлюза
        dist_g = {target_gate: 0}
        q = deque([target_gate])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_g:
                    dist_g[v] = dist_g[u] + 1
                    q.append(v)

        # Соседи вируса, ведущие к target_gate по кратчайшему пути
        next_candidates = []
        for nb in graph[virus]:
            if nb.isupper():
                continue  # вирус не ходит в шлюзы
            if dist_g.get(nb, -1) == dist_g.get(virus, -2) - 1:
                next_candidates.append(nb)

        if not next_candidates:
            break
        next_virus = min(next_candidates)

        # === 3. Отключить лексикографически наименьший коридор от target_gate ===
        corridors = []
        for nb in graph[target_gate]:
            if not nb.isupper():
                corridors.append((target_gate, nb))

        if not corridors:
            # Шлюз уже отключён — просто двигаемся
            virus = next_virus
            continue

        corridors.sort()
        gate, node = corridors[0]
        result.append(f"{gate}-{node}")
        # Отключаем
        graph[gate].discard(node)
        graph[node].discard(gate)

        # === 4. Вирус делает ход ===
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