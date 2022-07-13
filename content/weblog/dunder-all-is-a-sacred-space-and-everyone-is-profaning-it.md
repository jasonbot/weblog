+++
title =  "__all__ is a Sacred Space and you Murderous Goblins are all Profaning it"
date = 2021-03-31T00:00:00-08:00
tags = ["python"]
featured_image = ""
description = "You're all bad. None of you are free from sin."
+++

Let me spell something out for you trickster-meanies:

```python
# HELLO I AM thingy.py
__all__ = [X, Y, Z]

X = True
Y = True
Z = True
```

Reasonable, right?

```python
>>> from thingy import *
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/scheirer/thingy.py", line 1, in <module>
    __all__ = [X, Y, Z]
NameError: name 'X' is not defined
```

Python is older than my son (who is 3) and yet you abuse it. You monsters. You goblins. You haters. You fuckerinos.

Look: `__all__` is a list of GOD DAMN STRING IDENTIFIERS, NOT ACTUAL OBJECTS, AND IT INFORMS A PATTERN YOU RIGHTFULLY DON'T USE BECAUSE YOU NEVER SEE THAT `NameError`.

`__all__` is `['X', 'Y', 'Z']` and not your list of variable names, it's your list of export names.

`__all__` is, and has always been, [a list of *STRINGS* to be exported from your idiot module](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package) into your idiot notebook.

Oh my god my irrational hate has fueled in me a series of topics I care to "engage" about (COMMENTS DISABLED).