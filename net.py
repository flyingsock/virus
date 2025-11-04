from heapq import heappush, heappop


class Net:
    """
    Сеть корридоров
    """
    def __init__(self, adjacency: dict[str, set[str]]):
        """
        :param adjacency: список связности
        """
        self.adjacency = adjacency

    def choose_gate_path(self, start: str) -> list[str]:
        """
        Поиск пути в к ближайшему шлюзу
        :param start: вершина, c которой начинаетс поиск
        :return: список вершин, из которых состоит путь. Может быть пустым - это означает, что доступных шлюзов нет
        """
        visited = set()

        queue = []
        heappush(queue, (ord(start), start))

        path = list()
        while len(queue) > 0:
            _, node = heappop(queue)

            if node not in visited:
                visited.add(node)

            if node.isupper():
                path.append(node)
                return path

            neighbours = self.adjacency.get(node, [])
            if len(neighbours) != 0:
                path.append(node)

            for neighbour in neighbours:
                if neighbour not in visited:
                    heappush(queue, (ord(neighbour), neighbour))

        return []

    def close_gateway(self, gate_node: str, gate: str):
        """
        Отключить шлюз
        :param gate_node: вершина, инцидентная шлюзу
        :param gate: шлюз
        """
        if gate_node not in self.adjacency:
            return

        self.adjacency[gate_node].remove(gate)


def build_net(edges: list[tuple[str, str]]) -> Net:
    """
    :param edges: список рёбер (вершина, вершина)
    :return: сеть, составленная по списку рёбер
    """
    adjacency = {}

    for edge in edges:
        start, end = edge

        if start.isupper():
            start, end = end, start

        if start not in adjacency:
            adjacency[start] = []

        adjacency[start].append(end)

    return Net(adjacency)
