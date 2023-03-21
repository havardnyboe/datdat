def midline(table, labels, max_item_len=0):
    if not max_item_len:
        for row in table:
            for line in row:
                if len(line) > max_item_len:
                    max_item_len = len(line)

    for i in range(len(labels)):
        print("+", end="")
        print("-" * (max([len(labels[i]), max_item_len]) + 2), end="")
    print("+", end="")
    print()

    return max_item_len


def print_items(items, labels, max_item_len):
    for i, item in enumerate(items):
        print("|", end="")
        print(f" {item:<{max([len(labels[i]), max_item_len])}} ", end="")
    print("|", end="")
    print()


def print_table(table, labels):
    max_item_len = midline(table, labels)
    print_items(labels, labels, max_item_len)
    midline(table, labels, max_item_len)

    for row in table:
        print_items(row, labels, max_item_len)
    midline(table, labels, max_item_len)
