import pathlib
import glob

import match_o_matic_tree

transforms = {"match-o-matic.html": match_o_matic_tree.inject}

for filename in glob.glob(str(pathlib.Path(__file__).parent.absolute() / "*.html")):
    out_fn = str(
        pathlib.Path(__file__).parent.parent
        / "content"
        / (pathlib.Path(filename).name.replace(".html", "") + ".md")
    )

    print(filename, "->", out_fn)

    with open(filename) as in_handle:
        core = in_handle.read()

    within = ["<body>", "</body>"]

    body = core[core.index(within[0]) + len(within[0]) :]
    body = body[: body.index(within[1])]
    fn = filename.split("/")[-1]

    if fn in transforms:
        print("    transforming...")
        body = transforms[fn](body)

    with open(out_fn, "r") as in_handle:
        inner_body = in_handle.read()

    within = ["{{< raw >}}", "{{< /raw >}}"]
    start_part = inner_body[: inner_body.index(within[0]) + len(within[0])]
    end_part = inner_body[inner_body.index(within[1]) :]

    content = start_part + body + end_part

    with open(out_fn, "w") as out_handle:
        out_handle.write(content)
