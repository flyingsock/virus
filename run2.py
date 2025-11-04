import sys
from collections import deque


def is_gate(node: str) -> bool:
    return node.isupper()


def bfs_distances(graph, start):
    """Возвращает словарь расстояний от start до всех достижимых узлов."""
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
    """Возвращает следующую позицию вируса согласно правилам."""
    dist_from_virus = bfs_distances(graph, virus_pos)

    # Собираем все шлюзы и их расстояния
    gate_distances = {}
    for node, d in dist_from_virus.items():
        if is_gate(node):
            gate_distances[node] = d

    if not gate_distances:
        return None  # Вирус изолирован

    min_dist = min(gate_distances.values())
    # Выбираем лексикографически наименьший шлюз с минимальным расстоянием
    target_gate = min(gate for gate, d in gate_distances.items() if d == min_dist)

    # Получаем расстояния от целевого шлюза ко всем узлам
    dist_from_gate = bfs_distances(graph, target_gate)

    # Соседи текущей позиции, лежащие на кратчайшем пути к target_gate
    candidates = []
    for neighbor in graph[virus_pos]:
        # Проверяем: лежит ли neighbor на кратчайшем пути?
        if (neighbor in dist_from_virus and
                neighbor in dist_from_gate and
                dist_from_virus[neighbor] == dist_from_virus[virus_pos] + 1 and
                dist_from_gate[neighbor] == min_dist - 1):
            candidates.append(neighbor)

    if not candidates:
        # Fallback: просто выбираем любого соседа, ведущего к шлюзам (редкий случай)
        for neighbor in sorted(graph[virus_pos]):
            # Проверим, есть ли путь от neighbor до любого шлюза
            dist_nb = bfs_distances(graph, neighbor)
            if any(is_gate(n) for n in dist_nb):
                return neighbor
        # Если совсем нет — выбираем лексикографически наименьшего соседа
        return min(graph[virus_pos])

    return min(candidates)  # лексикографически наименьший


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

    # Основной цикл симуляции
    while True:
        # Соберём все возможные коридоры для отключения: (gate, node)
        candidates = []
        for node in graph:
            if is_gate(node):
                for neighbor in graph[node]:
                    if not is_gate(neighbor):  # только gate - обычный узел
                        candidates.append((node, neighbor))
        candidates.sort()  # лексикографическая сортировка: сначала по gate, потом по node

        chosen_action = None
        new_virus_pos = None

        # Перебираем кандидатов в порядке возрастания
        for gate, node in candidates:
            # Создаём временную копию графа
            temp_graph = {k: set(v) for k, v in graph.items()}
            # Удаляем коридор gate-node
            temp_graph[gate].discard(node)
            temp_graph[node].discard(gate)

            # Симулируем ход вируса
            next_pos = find_next_virus_position(temp_graph, virus_pos)

            # Если вирус изолирован — отлично
            if next_pos is None:
                chosen_action = (gate, node)
                new_virus_pos = None
                break

            # Проверяем: не находится ли next_pos рядом со шлюзом?
            # Если да — на следующем ходу вирус достигнет шлюза → проигрыш
            safe = True
            for nb in temp_graph.get(next_pos, []):
                if is_gate(nb):
                    safe = False
                    break

            if safe:
                chosen_action = (gate, node)
                new_virus_pos = next_pos
                break

        # По условию всегда есть решение, так что chosen_action не None
        gate, node = chosen_action
        result.append(f"{gate}-{node}")

        # Применяем отключение к основному графу
        graph[gate].discard(node)
        graph[node].discard(gate)
        virus_pos = new_virus_pos

        # Если вирус изолирован — завершаем
        if virus_pos is None:
            break

        # Дополнительная проверка: если из текущей позиции нет путей до шлюзов — выход
        dist_check = bfs_distances(graph, virus_pos)
        if not any(is_gate(node) for node in dist_check):
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            parts = line.split('-')
            if len(parts) == 2:
                node1, node2 = parts
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()