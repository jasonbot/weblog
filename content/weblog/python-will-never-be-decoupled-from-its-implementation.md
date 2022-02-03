+++
title =  "Python as a Language is Unescabably Coupled with its Implementation Part 1: LET'S DO DUMB SHIT WITH THE GC"
date = 2021-04-04T00:00:00-08:00
tags = ["python"]
featured_image = ""
description = "__dict__, lol"
+++

There is a convenient but untrue fiction about Python that the language specification is somehow cleanroom and CPython is actually "just an implementation."

This has always been false, and harmful at best.

Look at `__dict__`. Near every Python object has a dictionary that fuels and consumes it. All your dotted getters are mere passthroughs for dot `__getitem__`ers.

Another fun thing is the leaking of implementation details in Bad Ways. Here's something you _can_ do but _should not_ do, lest I find out where you live and poop in your mailbox:

```python
import gc

x = "HELLO"
print("My names are:", [[key for key, value in var.items() if value is x] for var in gc.get_referrers(x)])
My names are: [['x']]
```

You _could_ create a class where all its instances know their names. All their names. Do not do this. I will leave you poop.