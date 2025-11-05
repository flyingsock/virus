import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    edges = [(u.strip(), v.strip()) for u, v in edges]

    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    gates = {node for node in graph if node.isupper()}
    virus = 'a'
    result = []

    while True:
        # === Симулируем ход вируса (без отключения) ===
        # Найти текущую цель
        dist_v = {virus: 0}
        q = deque([virus])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_v:
                    dist_v[v] = dist_v[u] + 1
                    q.append(v)

        reachable_gates = {g: dist_v[g] for g in gates if g in dist_v}
        if not reachable_gates:
            break

        min_d = min(reachable_gates.values())
        target_gate = min(g for g, d in reachable_gates.items() if d == min_d)

        # BFS from target_gate
        dist_g = {target_gate: 0}
        q = deque([target_gate])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_g:
                    dist_g[v] = dist_g[u] + 1
                    q.append(v)

        # Найти следующую позицию вируса
        next_pos = None
        current_d = dist_g.get(virus, float('inf'))
        for nb in graph[virus]:
            if nb.isupper():
                continue
            if dist_g.get(nb, float('inf')) == current_d - 1:
                if next_pos is None or nb < next_pos:
                    next_pos = nb

        if next_pos is None:
            break

        # === Проверяем: будет ли вирус рядом со шлюзом после хода? ===
        imminent_gates = []
        for nb in graph[next_pos]:
            if nb.isupper() and nb in graph and next_pos in graph[nb]:
                imminent_gates.append(nb)

        if imminent_gates:
            # Должны отключить коридор от одного из этих шлюзов
            imminent_gates.sort()
            gate = imminent_gates[0]
            # Выбрать лексикографически наименьший коридор от gate
            nodes = [nb for nb in graph[gate] if not nb.isupper()]
            if nodes:
                nodes.sort()
                node = nodes[0]
                result.append(f"{gate}-{node}")
                graph[gate].discard(node)
                graph[node].discard(gate)
            # Если нет коридоров — значит, уже отключён, но по условию этого не будет
        else:
            # Нет угрозы — отключаем лексикографически наименьший коридор вообще
            candidates = []
            for gate in gates:
                for nb in graph[gate]:
                    if not nb.isupper():
                        candidates.append((gate, nb))
            if candidates:
                candidates.sort()
                gate, node = candidates[0]
                result.append(f"{gate}-{node}")
                graph[gate].discard(node)
                graph[node].discard(gate)
            else:
                break

        # Теперь применяем настоящий ход вируса
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