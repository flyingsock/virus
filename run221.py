import sys
from collections import deque


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
        if (neighbor in dist_from_virus and
                neighbor in dist_from_gate and
                dist_from_virus[neighbor] == dist_from_virus[virus_pos] + 1 and
                dist_from_gate[neighbor] == min_dist - 1):
            candidates.append(neighbor)

    return min(candidates) if candidates else None


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # Построим граф как словарь множеств
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = set()
        if v not in graph:
            graph[v] = set()
        graph[u].add(v)
        graph[v].add(u)

    virus_pos = 'a'
    result = []

    while True:
        # Собираем все возможные коридоры для отключения: (шлюз, обычный_узел)
        candidates = []
        for node in graph:
            if is_gate(node):
                for neighbor in graph[node]:
                    if not is_gate(neighbor):
                        candidates.append((node, neighbor))

        # Если нет коридоров шлюзов — задача решена
        if not candidates:
            break

        # Сортируем лексикографически: сначала по шлюзу, потом по узлу
        candidates.sort()

        # Выбираем первое действие (гарантированно безопасное по условию задачи)
        gate, node = candidates[0]
        result.append(f"{gate}-{node}")

        # Применяем отключение в основном графе
        graph[gate].discard(node)
        graph[node].discard(gate)

        # Симулируем ход вируса в обновлённом графе
        next_pos = find_next_virus_position(graph, virus_pos)
        if next_pos is None:
            break  # Вирус изолирован
        virus_pos = next_pos

        # Дополнительная проверка: если из текущей позиции нет путей до шлюзов — завершаем
        dist_check = bfs_distances(graph, virus_pos)
        if not any(is_gate(n) for n in dist_check):
            break

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