import csv
import os
import timeit
from typing import Dict, List

from BTrees.OOBTree import OOBTree


def load_items(filename: str) -> List[Dict]:
    """Завантажує товари з CSV-файлу."""
    items = []

    with open(filename, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["Price"] = float(row["Price"])
            items.append(row)

    return items


def add_item_to_tree(tree: OOBTree, item: Dict) -> None:
    """
    Додає товар до OOBTree.

    Ключем є ціна товару. Якщо кілька товарів мають однакову ціну,
    вони зберігаються в одному списку.
    """
    price = item["Price"]

    if price not in tree:
        tree[price] = []

    products = list(tree[price])
    products.append(item)
    tree[price] = products


def add_item_to_dict(items_dict: Dict, item: Dict) -> None:
    """Додає товар до словника за його унікальним ID."""
    items_dict[item["ID"]] = item


def range_query_tree(
    tree: OOBTree,
    min_price: float,
    max_price: float,
) -> List[Dict]:
    """Повертає товари з OOBTree у заданому діапазоні цін."""
    result = []

    for _, products in tree.items(min_price, max_price):
        result.extend(products)

    return result


def range_query_dict(
    items_dict: Dict,
    min_price: float,
    max_price: float,
) -> List[Dict]:
    """Повертає товари зі словника у заданому діапазоні цін."""
    return [
        item
        for item in items_dict.values()
        if min_price <= item["Price"] <= max_price
    ]


def main() -> None:
    filename = "generated_items_data.csv"

    if not os.path.exists(filename):
        print(
            f"Файл {filename} не знайдено.\n"
            "Додайте CSV-файл до тієї самої папки, що й task2.py."
        )
        return

    items = load_items(filename)

    tree = OOBTree()
    items_dict = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(items_dict, item)

    min_price = 10.0
    max_price = 100.0
    query_count = 100

    tree_result = range_query_tree(tree, min_price, max_price)
    dict_result = range_query_dict(items_dict, min_price, max_price)

    if len(tree_result) != len(dict_result):
        raise ValueError(
            "OOBTree і dict повернули різну кількість товарів."
        )

    tree_time = timeit.timeit(
        lambda: range_query_tree(tree, min_price, max_price),
        number=query_count,
    )

    dict_time = timeit.timeit(
        lambda: range_query_dict(items_dict, min_price, max_price),
        number=query_count,
    )

    print(f"Кількість завантажених товарів: {len(items)}")
    print(
        f"Товарів у діапазоні від {min_price} до {max_price}: "
        f"{len(tree_result)}"
    )
    print(
        f"Total range_query time for OOBTree: "
        f"{tree_time:.6f} seconds"
    )
    print(
        f"Total range_query time for Dict: "
        f"{dict_time:.6f} seconds"
    )

    if tree_time < dict_time:
        difference = dict_time / tree_time
        print(f"OOBTree швидше приблизно у {difference:.2f} разів.")
    else:
        difference = tree_time / dict_time
        print(f"Dict швидше приблизно у {difference:.2f} разів.")


if __name__ == "__main__":
    main()
