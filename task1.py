import networkx as nx
from tabulate import tabulate


SOURCE = "Джерело"
SINK = "Сток"


def build_graph() -> nx.DiGraph:
    """
    Створює орієнтований граф логістичної мережі.
    """

    graph = nx.DiGraph()

    edges = [
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),

        ("Термінал 2", "Склад 2", 10),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),

        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),

        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),

        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),

        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]

    for source, target, capacity in edges:
        graph.add_edge(source, target, capacity=capacity)

    # Суперджерело об'єднує два термінали.
    graph.add_edge(SOURCE, "Термінал 1", capacity=60)
    graph.add_edge(SOURCE, "Термінал 2", capacity=55)

    # Суперстік об'єднує всі магазини.
    for store_number in range(1, 15):
        graph.add_edge(
            f"Магазин {store_number}",
            SINK,
            capacity=float("inf"),
        )

    return graph


def calculate_max_flow(
    graph: nx.DiGraph,
) -> tuple[int, dict]:
    """
    Обчислює максимальний потік алгоритмом Едмондса-Карпа.
    """

    flow_value, flow_dict = nx.maximum_flow(
        graph,
        SOURCE,
        SINK,
        flow_func=nx.algorithms.flow.edmonds_karp,
    )

    return flow_value, flow_dict


if __name__ == "__main__":
    graph = build_graph()
    max_flow, flow_data = calculate_max_flow(graph)

    print(f"Кількість вершин: {graph.number_of_nodes()}")
    print(f"Кількість ребер: {graph.number_of_edges()}")
    print(f"Максимальний потік: {max_flow} одиниць")
