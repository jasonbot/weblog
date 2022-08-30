+++
title =  "A Case for Match"
date = 2022-08-26T00:00:00-00:00
tags = ["python"]
featured_image = ""
description = "Match, point"
+++

The Python 3.10 release includes the [new `match` statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement), which superficially looks like the `case`/`switch` statements in other languages but semantically is closer to pattern matching in [Haskell](http://learnyouahaskell.com/syntax-in-functions) or [Rust](https://doc.rust-lang.org/book/ch18-03-pattern-syntax.html).

Like the [walrus operator](https://docs.python.org/3/reference/expressions.html#assignment-expressions)*, I struggled to find a use case for this and it seemed like a feature that was added just because the language is 30+ years old and all the _good_ new functionality is taken.

However, I found a pretty good case for it that used to be a lot more work: duck-typey arguments that make default case rules easy but enable more complex functionality as needed.

Namely, I'm writing a REST API at work that is _mostly_ CRUD, but for historical reasons certain field names in JSON payloads do not match up with their ORM equivalents (which in turn may not match up with their DB column equivalents).

First off, we get a dict and want to just specify the keys we care about:

```python3
import typing

def copy_keys(input: dict, keep_keys: typing.Iterable[typing.Hashable]):
   keep_set = set(keep_keys)

   return {k: v for k, v in input.items() if k in keep_set}

x = {'a': 1, 'b': 2, 'c': 3}

print(copy_keys(x, ['a', 'c']))
# {'a': 1, 'c': 3}
```

Simple enough. Now what if we need to _remap_ our keys?

```python3
print(copy_keys(x, ['a', ('c', 'b')]))  # We want:{'a': 1, 'b': 3}
```

Well, we can use pattern matching:

```python3
import typing

def copy_keys(input: dict, keep_keys: typing.Iterable[typing.Hashable | typing.Tuple[typing.Hashable, typing.Hashable]]):
    keep_map = {}
    for item in keep_keys:
        match item:
            case (from_key, to_key):
                keep_map[from_key] = to_key
            case key:
                keep_map[key] = key
    print(keep_map)

    return {keep_map[k]: v for k, v in input.items() if k in keep_map}

x = {'a': 1, 'b': 2, 'c': 3}

print(copy_keys(x, ['a', ('c', 'b')]))  # {'a': 1, 'b': 3}
```

Simpler than the `isinstance(x, tuple) and len(x) == 2` dance we'd have to do in prior Pythons. The `match` statement can help write library code that is clean and easy to use while at the same time being clear and less magical than it would have been in previous Pythons.

\* The one case I have come up with for Walrus that makes sense:

```python3
if (x := do_something()) is not None:
    x.do_something_else()
```