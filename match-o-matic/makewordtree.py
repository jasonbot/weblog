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

with open("index.html", "r") as in_handle:
    core = in_handle.read()
    starty = "const rootWordNode = "

    startpt = core[:(core.index(starty) + len(starty))]
    endy = core.index(";", core.index(starty))
    endpt = core[endy:]

    core = startpt + json_tree + endpt


with open("index.html", "w") as out_handle:
    out_handle.write(core)

within = ["<body>", "</body>"]

body = core[core.index(within[0]) + len(within[0]):]
body = body[:body.index(within[1])]

with open("../content/match-o-matic.md", "r") as in_handle:
    inner_body = in_handle.read()

within = ["{{< raw >}}", "{{< /raw >}}"]
start_part = inner_body[:inner_body.index(within[0]) + len(within[0])]
end_part = inner_body[inner_body.index(within[1]):]

content = start_part + body + end_part

with open("../content/match-o-matic.md", "w") as out_handle:
    out_handle.write(content)