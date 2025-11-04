import sys
from collections import deque, defaultdict


def is_gateway(node: str) -> bool:
    return node.isupper()


def build_graph(edges):
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


def bfs_distances(graph, start, targets):
    if not targets:
        return {}
    queue = deque([(start, 0)])
    dist = {start: 0}
    found = {}
    while queue:
        node, d = queue.popleft()
        if node in targets:
            found[node] = d
        for nb in graph[node]:
            if nb not in dist:
                dist[nb] = d + 1
                queue.append((nb, d + 1))
    return found


def get_next_move(graph, current, gateways):
    distances = bfs_distances(graph, current, gateways)
    if not distances:
        return None
    min_dist = min(distances.values())
    closest_gateways = [g for g, d in distances.items() if d == min_dist]
    target_gateway = min(closest_gateways)

    # Compute distances from target_gateway to all nodes
    queue = deque([(target_gateway, 0)])
    dist_to_target = {target_gateway: 0}
    while queue:
        node, d = queue.popleft()
        for nb in graph[node]:
            if nb not in dist_to_target:
                dist_to_target[nb] = d + 1
                queue.append((nb, d + 1))

    candidates = []
    for nb in graph[current]:
        if nb in dist_to_target and dist_to_target[nb] == min_dist - 1:
            candidates.append(nb)
    if not candidates:
        return None
    return min(candidates)


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = build_graph(edges)
    all_nodes = set()
    for u, v in edges:
        all_nodes.add(u)
        all_nodes.add(v)
    gateways = {node for node in all_nodes if is_gateway(node)}
    virus_pos = 'a'
    result = []

    while True:
        # Determine active gateways (still connected to the graph)
        active_gateways = set()
        for g in gateways:
            if g in graph and any(not is_gateway(nb) for nb in graph[g]):
                active_gateways.add(g)

        if not active_gateways:
            break

        # Find reachable gateways from current virus position
        distances = bfs_distances(graph, virus_pos, active_gateways)
        if not distances:
            break

        min_dist = min(distances.values())
        closest_gateways = [g for g, d in distances.items() if d == min_dist]
        target_gateway = min(closest_gateways)

        # Collect all active edges from target_gateway to regular nodes
        candidates = []
        if target_gateway in graph:
            for nb in graph[target_gateway]:
                if not is_gateway(nb):
                    candidates.append((target_gateway, nb))

        if not candidates:
            # Gateway is already isolated; move virus and continue
            next_pos = get_next_move(graph, virus_pos, active_gateways)
            if next_pos is None:
                break
            virus_pos = next_pos
            continue

        # Choose lexicographically smallest edge
        candidates.sort(key=lambda x: (x[0], x[1]))
        chosen = candidates[0]

        # Disconnect the edge
        result.append(f"{chosen[0]}-{chosen[1]}")
        graph[chosen[0]].discard(chosen[1])
        graph[chosen[1]].discard(chosen[0])

        # Move virus
        next_pos = get_next_move(graph, virus_pos, active_gateways)
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