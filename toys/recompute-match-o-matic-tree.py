import collections
import json


class node(list):
    def __init__(self):
        self.extend([False, collections.defaultdict(node)])


root = node()

for line in open("wordlist.txt"):
    branch = root
    for letter in line.strip():
        branch = branch[1][letter]
    branch[0] = True

json_tree = json.dumps(root)

with open("match-o-matic.html", "r") as in_handle:
    core = in_handle.read()
    starty = "const rootWordNode = "

    startpt = core[: (core.index(starty) + len(starty))]
    endy = core.index(";", core.index(starty))
    endpt = core[endy:]

    core = startpt + json_tree + endpt


with open("match-o-matic.html", "w") as out_handle:
    out_handle.write(core)
