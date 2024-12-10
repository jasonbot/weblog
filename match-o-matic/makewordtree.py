import collections
import json

class node(list):
    def __init__(self):
        self.extend([False, collections.defaultdict(node)])


root = node()

for line in open('wordlist.txt'):
    branch = root
    for letter in line.strip():
        branch = branch[1][letter]
    branch[0] = True

print(json.dumps(root))