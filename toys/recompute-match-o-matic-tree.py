import collections
import json


class node(list):
    def __init__(self):
        self.extend([0, collections.defaultdict(node)])


root = node()

letters = set()

for line in open("wordlist.txt"):
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

with open("match-o-matic.html", "r") as in_handle:
    core = in_handle.read()
    starty = "const rootWordNode = "

    startpt = core[: (core.index(starty) + len(starty))]
    endy = core.index(";", core.index(starty))
    endpt = core[endy:]

    core = startpt + json_tree + endpt


with open("match-o-matic.html", "w") as out_handle:
    out_handle.write(core)
