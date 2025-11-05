import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # Очистка от пробелов
    edges = [(u.strip(), v.strip()) for u, v in edges]

    graph = defaultdict(set)
    gates = set()
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
        if u.isupper():
            gates.add(u)
        if v.isupper():
            gates.add(v)

    virus = 'a'
    result = []

    while True:
        # BFS от вируса
        dist = {virus: 0}
        q = deque([virus])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)

        # Найти шлюзы на минимальном расстоянии
        min_d = float('inf')
        closest_gates = []
        for gate in gates:
            if gate in dist:
                if dist[gate] < min_d:
                    min_d = dist[gate]
                    closest_gates = [gate]
                elif dist[gate] == min_d:
                    closest_gates.append(gate)

        if not closest_gates:
            break

        closest_gates.sort()

        # Собрать ВСЕ коридоры от этих шлюзов
        candidates = []
        for gate in closest_gates:
            for nb in graph[gate]:
                if not nb.isupper():
                    candidates.append((gate, nb))

        if not candidates:
            # Все коридоры отключены — двигаем вирус и продолжаем
            # Найдем следующую позицию (к любому из closest_gates)
            target_gate = closest_gates[0]
            # BFS от target_gate
            dist_gate = {target_gate: 0}
            q = deque([target_gate])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if v not in dist_gate:
                        dist_gate[v] = dist_gate[u] + 1
                        q.append(v)
            next_pos = None
            current_d = dist_gate.get(virus, float('inf'))
            for nb in graph[virus]:
                if not nb.isupper() and dist_gate.get(nb, float('inf')) == current_d - 1:
                    if next_pos is None or nb < next_pos:
                        next_pos = nb
            if next_pos is None:
                break
            virus = next_pos
            continue

        # Выбираем лексикографически наименьший коридор
        candidates.sort()
        gate, node = candidates[0]
        result.append(f"{gate}-{node}")
        graph[gate].discard(node)
        graph[node].discard(gate)

        # Двигаем вирус к лексикографически наименьшему шлюзу из closest_gates
        target_gate = closest_gates[0]
        dist_gate = {target_gate: 0}
        q = deque([target_gate])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_gate:
                    dist_gate[v] = dist_gate[u] + 1
                    q.append(v)

        next_pos = None
        current_d = dist_gate.get(virus, float('inf'))
        for nb in graph[virus]:
            if nb.isupper():
                continue
            if dist_gate.get(nb, float('inf')) == current_d - 1:
                if next_pos is None or nb < next_pos:
                    next_pos = nb

        if next_pos is None:
            break
        virus = next_pos

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