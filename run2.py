import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    edges = [(u.strip(), v.strip()) for u, v in edges]
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    gates = {n for n in graph if n.isupper()}
    virus = 'a'
    result = []

    while True:
        # Get all gate links
        candidates = []
        for gate in gates:
            for nb in graph[gate]:
                if not nb.isupper():
                    candidates.append((gate, nb))
        if not candidates:
            break

        # BFS from virus
        dist = {virus: 0}
        q = deque([virus])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)

        # Find gates at distance 1
        threat = []
        for gate in gates:
            if gate in dist and dist[gate] == 1:
                threat.append(gate)

        if threat:
            threat.sort()
            gate = threat[0]
        else:
            candidates.sort()
            gate = candidates[0][0]

        # Cut lex smallest link from gate
        links = [nb for nb in graph[gate] if not nb.isupper()]
        if not links:
            break
        links.sort()
        node = links[0]
        result.append(f"{gate}-{node}")
        graph[gate].discard(node)
        graph[node].discard(gate)

        # Move virus
        dist = {virus: 0}
        q = deque([virus])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)

        reachable_gates = {g: dist[g] for g in gates if g in dist}
        if not reachable_gates:
            break
        min_d = min(reachable_gates.values())
        target = min(g for g, d in reachable_gates.items() if d == min_d)

        dist_gate = {target: 0}
        q = deque([target])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in dist_gate:
                    dist_gate[v] = dist_gate[u] + 1
                    q.append(v)

        next_v = None
        for nb in graph[virus]:
            if nb.isupper():
                continue
            if dist_gate.get(nb, -1) == dist_gate.get(virus, -2) - 1:
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
            parts = line.split('-')
            if len(parts) == 2:
                edges.append((parts[0], parts[1]))
    result = solve(edges)
    for r in result:
        print(r)


if __name__ == "__main__":
    main()