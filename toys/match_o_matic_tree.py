import collections
import json


class node(list):
    def __init__(self):
        self.extend([0, collections.defaultdict(node)])


def inject(source_code, filename="wordlist.txt"):
    root = node()

    letters = set()

    for line in open(filename):
        branch = root
        for letter in line.strip():
            branch = branch[1][letter]
            if letter.isalpha():
                letters.add(letter)
        branch[0] = 1

    json_tree = json.dumps(root, separators=(",", ":"))
    for l in letters:
        json_tree = json_tree.replace(f'"{l}":', f"{l}:")

    json_tree = json_tree.replace("[1,{}]", "[1]")

    starty = "const rootWordNode = "

    startpt = source_code[: (source_code.index(starty) + len(starty))]
    endy = source_code.index(";", source_code.index(starty))
    endpt = source_code[endy:]

    return startpt + json_tree + endpt


if __name__ == "__main__":
    with open("match-o-matic.html") as in_handle:
        source = in_handle.read()

    with open("match-o-matic.html", "w") as out_handle:
        out_handle.write(inject(source, "smalllist.txt"))
