import csv
import timeit
from BTrees.OOBTree import OOBTree


def load_items(filename):
    """
    Завантажує товари з CSV-файлу.
    """
    items = []

    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["Price"] = float(row["Price"])
            items.append(row)

    return items


def add_item_to_tree(tree, item):
    tree[item["ID"]] = item


def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = item


def range_query_tree(tree, min_price, max_price):
    result = []

    for _, item in tree.items():
        if min_price <= item["Price"] <= max_price:
            result.append(item)

    return result


def range_query_dict(dictionary, min_price, max_price):
    result = []

    for item in dictionary.values():
        if min_price <= item["Price"] <= max_price:
            result.append(item)

    return result
