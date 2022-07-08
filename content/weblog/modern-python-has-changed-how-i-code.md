+++
title =  "Modern Python has Changed How I Code"
date = 2022-07-07T00:00:00-08:00
tags = ["python", "programming"]
featured_image = ""
description = "Python: Still Kicking, Still More to Learn"
+++

I can't understate the importance of how much the following have changed and improved the way I write Python and have confidence in its correctness:

* [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration)
* [Black](https://github.com/psf/black)
* [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
* [Mypy](http://mypy-lang.org/)
* [Type Hints](https://docs.python.org/3/library/typing.html)

## Continuous Integration

This isn't particularly new to me (or the industry), but a good CI workflow that runs tests and linting _on every commit pushed to the repo tracker_ gives confidence that the code is clean to merge into the main branch. Generally you build up stages as your org progresses:

* Run unit tests
* Run and enforce code coverage standards
* Run lint
* Run style checks

## Black

About two years into writing Go I started using [`gofmt`](https://go.dev/blog/gofmt) to help me clean up a bunch of pre-Go-1.0 code that [still used semicolons](https://go.dev/doc/effective_go#semicolons). I turned on fomrat on save in my editor and never turned it off. A large point of contention over the course of my career is arguing with senior developers over bikesheddy, arbitrary, often cruel and capricious code style standards over the actual semantic behavior of the code.

Then I found [Prettier](https://prettier.io/) while writing some JSX/React code. While it had knobs to tweak most people didn't tweak them. It made the code I worked with more readable and I got the same delight out of using it as I did `gofmt`.

I was sold on opinionated formatting.

Now I use Black on all my code, auto format on save, and also enforce linter rules in CI to make sure that all code is Black-formatted.


Agreeing on a format and enforcing it makes code diffs purely _semantic_ and no longer _stylistic_. This makes code review less painful and shuts down completely unproductive conversations on where commas go. 

Blackening your codebase initially is admittedly ugly and somewhat destructive as you pollute your repo history with the reformat commits and it makes most tools that do line history barf. That part sucks and I don't know a good way around it, but it does make the path forward so much more pleasant one that band-aid comes off.

## Dataclasses

Over the years there have been _so many_ attempts to do data structures in Python, all equally bad and weird: [marshmallow](https://marshmallow.readthedocs.io/en/stable/), [colander](https://docs.pylonsproject.org/projects/colander/en/latest/index.html), [schematics](https://schematics.readthedocs.io/en/latest/),  stdlib [struct](https://docs.python.org/3/library/struct.html), the list goes on.

One of the "warts" of the language is that dictionaries were not guaranteed to be in any order, and add on that the fact that to avoid hash collision attacks every Python process seeds its hashing algorithm with a random number, even the out-of-order iteration order would change from run to run.

Enter [Python 3.7](https://docs.python.org/3/whatsnew/3.7.html) officially announcing that an implementation detail in 3.6 was now standard behavior: dict traversal would be ordered.

So now built into the standard library is an easy, in-order way to define a data struct in the [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) library.

```python3
import dataclasses
import typing as T

@dataclasses.dataclass
class MyStruct:
    field_1: str = "default"
    field_2: int
    field_3: T.List[str]
```

That's not a lot of code to get a very powerful, good enough abstraction over data structures. It even has options to make the classes immutable (`frozen`) and implements `__slots__` to make large numbers of them more memory efficient.

These things are a godsend, along with typing below.

## Mypy

Another tool I add to my CI, I run the Mypy tool over my code as I incrementally add type hints to ensure the code is correct. And since it can be done implicitly, your library code can look like this:

```python3
def thing_with_strings(a: str, b: str) -> str:
    return a + b
```

then your consuming app logic code can do this, unannotated:

```python3
def my_app_logic():
    x = "hello"
    y = 5
    thing_with_strings(x, y)
```

and Mypy will deduce the types and yell at you that `y` is the wrong type. Annotating libraries, even if you don't touch the codebases that consume them, can help find errors right away.

## Type Hints

You don't have to go all in with typing, but when you do the [type annotation system](https://peps.python.org/pep-0484/) is good enough (though not nearly as rich as other languages'). In particular I find TypeVar to be clunky for doing generic coding, but it's easy to use and covers most cases. If anything, its limitations keep you from doing insane turing-complete stunts like C++ programmers like to do with template metaprogramming.

## That's All

These relatively minor changes to my Python coding I've made over the last 3-5 years have definitely made the language feel safer and quite a bit different than the unsafe, scary, let's-pass-opaque-dicts-around crazy party that made larger codebases unmaintainable and encourages Python library authors to do weird, abusive metaprogramming stuff in their code to make it more suitable "for humans."