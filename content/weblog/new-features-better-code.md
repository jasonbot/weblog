+++
title =  "Modern Python: New Features, Better Code"
date = 2022-08-29T00:00:00-08:00
tags = ["python", "programming"]
featured_image = ""
description = "Python: Yeah."
draft = true
+++

# Introduction
In the time I've been at Easypost, we've been putting continuous effort into making sure our code stays up-to-date to make sure we keep ahead of potential security and support issues, as well as to make our code easier to read, write and maintain as the Python language continues to mature.

# Black
The [Black code formatter](https://black.readthedocs.io/en/stable/) is a few years old now and [officially hosted by the PSF](https://github.com/psf/black). It follows the vein of [Gofmt](https://go.dev/blog/gofmt) (or, to a lesser degree, [Prettier](https://prettier.io/docs/en/index.html)) by being "opinionated" and having a reasonable set of defaults and few, if any, knobs that can be tweaked.

This has two immediately obvious advantages:

1. It silences non-constructive, bikesheddy, purely opinion-based code style comments
2. Since everything is uniformly formatted, diffs will be entirely _semantic_ and not _syntactic_, meaning diffs are about how the code's meaning has changed and not how the code's looks have changed.

We use Makefiles for most of our heavy lifting in the build-and-deploy process, so adding a mypy step in our services is pretty easy:

```makefile
## checkblack - Run black checks
checkblack:
        venv/bin/black --check --diff $(SERVICENAME)
```

# MyPy
> "The standard library is where modules go to die"
>
> Kenneth Reitz

MyPy is a tool used to analyze Python source and identify type errors/potential errors using type hints. While type hinting is largely built into the standard library/language spec, the actual enforcement of it is done by an external tool at build time. Why an external tool? Because Python typing is a work in progress still being iterated on, and having it as a core part of the language would slow down its development.

To enforce MyPy in test/lint steps, it's Makefiles to the rescue once more:

```makefile
## checkstatic - Run static checks
checkstatic:
        venv/bin/mypy $(SERVICENAME)
```

Then commonly-used build targets like make test can include these steps as dependencies.

# Continuous Integration

Not a new concept, but worth pointing out that both Black and Mypy analysis is done at Easypost during the lint step in our Continuous Integration process, so no code that fails automated style/type checks can get merged into the main branch.

# Type Hinting
The road to formal typing in Python started out with the [Abstract Base Class effort](https://peps.python.org/pep-3119/) many years ago and has progressed since then. ABCs started out as a way of formally defining collections of duck-typed methods as belonging to a specific 'protocol', like a map or an array or an iterator, and went from there. In this regard ABCs are very similar to Go's Interfaces.

[Type hinting](https://peps.python.org/pep-0484/) lets you incrementally update your code to enforce "good" data goes into it and avoids boneheaded errors that other languages don't let through by default. The good thing about incremental is it's incremental, meaning you don't have to go all-in at once but instead gradually get it right.

I cannot emphasize how much of a good idea this is: you still get the flexibility and speed of writing fluent Python when doing exploratory coding, and when your design solidified you can add type hints to give some confidence about the code _at the pace you wish to work at_. You do not have to go all or nothing.

In C++, by the time you get to your `main` function, because everything is explicitly typed and determined at compile time, you can get away with declaring most of your variables' types as `auto` (fight me). Similarly in Python, if your _library_ code is well typed, your _business logic_ that consumes it can have sparse (if any) type declarations and will still be safe since it can derive types from the code it's calling.

The basics of type hinting are easy. When you do a variable assignment, you can decorate it with a type:

```python3
a = "hello"       # Old and busted
a: str = "hello"  # New hotness
```

Function definitions can mark up what they expect and return:

```python3
def square(x: int) -> int:  # Takes an int, returns an int
    return x ** 2
```

Context managers use the comments to mark what the context manager gives you:

```python3
# See also: typing.IO, typing.TextIO
with open("hello.txt', "rb") as input_handle: # type: T.BinaryIO
    do_something_interesting(input_handle)
Custom types work as expected:
class MyCustomType:
    pass

x: MyCustomType = MyCustomType()
```

If something can be multiple types, you can use a Union. Python 3.10 has a nicer syntax for it with the pipe operator.

```python3
my_numeric: T.Union[int, float] = 5              # Or could be 5.0
my_numeric_in_python_3_10_plus: int | float = 5  # Moving toward this
```

For anything, use `Any`:

```python3
my_wildcard: T.Any = None  # THERE ARE NO RULES HERE DUDE
```

Not a great idea to litter your code with `Any` as it kind of violates the spirit of adding type annotations to your code, but it can be useful in an incremental process as you introduce types to your codebase.

Special case if you want something to be a value or None: you mark as Optional or union the type with None:

```python3
my_potentially_none: T.Optional[str] = "Hi"
my_potentially_none_3_10_plus: str | None = "Hi"
```

That breaks code that doesn't expect None:

```python3
import typing as T

def fn(x: str):
    print(x)

my_value: T.Optional[str] = "hello"

if my_value is not None:
    fn(my_value)
```

> `error: Argument 1 to "fn" has incompatible type "Optional[str]"; expected "str"`

You sometimes have explicitly mark with cast so that MyPy knows you're explicitly using one type over the other:

```python3
if my_value is not None:
    fn(T.cast(str, my_value))  # Now we know for sure it's not None
```

If you want to use Tuple as a type of Frozen List:

```python3
my_tuple: tuple[int] = (1, 2, 3, 4)
```

> `error: Incompatible types in assignment (expression has type "Tuple[int, int, int, int]", variable has type "Tuple[int]")`

It assumes a tuple of length 1 with a single `int`. You use this syntax with `Ellipsis` to say it's an arbitrary number of entries in the tuple:

```python3
my_tuple: tuple[int, ...] = (1, 2, 3, 4)
```

For the sake of brevity I will not get into [`TypeVar`s](https://docs.python.org/3/library/typing.html#typing.TypeVar), [`Protocol`s](https://docs.python.org/3/library/typing.html#typing.Protocol), or other recent improvements like [`ParamSpec`s](https://docs.python.org/3/library/typing.html#typing.ParamSpec) or [`Variadics`](https://peps.python.org/pep-0646/) (the latter of which excited me the most). The system for Python typing is a work-in-progress and with each new version of the language gets slightly better and more complete. It's not as good as the type systems in other languages, but it's good enough for industrial programming.

# Dataclasses
Doing data structures of any complexity has been a plain point for about as long as Python has been around. From the ancient days of [zope.schema](https://zopeschema.readthedocs.io/en/latest/) to more modern libraries like [marshmallow](https://marshmallow.readthedocs.io/en/stable/), [schematics](https://schematics.readthedocs.io/en/latest/), and [colander](https://docs.pylonsproject.org/projects/colander/en/latest/), the problem has a panoply of 'solutions,' each with their own individual quirks; some of which are obviated by the newer features of Python like annotations and [guaranteed in-order dictionary traversal](https://mail.python.org/pipermail/python-dev/2017-December/151283.html).

Dataclasses exist in the standard library. That's a huge plus because they don't require a third party library, tiny time bombs hiding away in your `requirements.txt` just waiting to introduce random CVEs at inopportune moments. Dataclasses are just enough data model for a lot of use cases.

```python3
import dataclasses

@dataclasses.dataclass
class PocketMonster:
  name: str
  # If a PocketMonster is instantiated without hit_points
  # specified, it will default to 4.
  hit_points: int = 4
```

As a bonus, you can make them immutable to employ some basic tenets of functional programming (and enhance testing):

```python3
import dataclasses

@dataclasses.dataclass(frozen=True)
class Pet:
    name str

my_cat = Pet(name="Spots")
# Your new name is Ham Sandwich. I'm am a cruel owner.
my_cat.name = "Ham Sandwich"
```

> `dataclasses.FrozenInstanceError: cannot assign to field 'name'`

This solves the problem of data provenance as well. One anti-pattern we have been attempting to get rid of from our codebase are functions like this:

```python3
def do_something_to_a_dict(data_dict: dict):
   # Mutate (or don't) in-place the data passed in
   dict['some_key'] = dict['some_other_key'] + data_from_the_internet()
   dict['other_key'] = int(dict['other_key'])
```

When a dictionary (which in Python is a bag of key/value anythings) starts to get changed willy-nilly over the course of its lifetime it gets _really hard to tell_ just _where_ and _when_ a speccific piece of data in the dictionary was created/modified.

So how do we go about mutating data _as needed_? One of two patterns:

1. In place with a `@property`:
    ```python3
    @dataclasses.dataclass(frozen=True)
    class Pet:
        name: str

        @property
        def what_you_say_to_get_its_attention(self):
            return self.name.upper() + "!!!"
    ```
2. Generating a copy using [the `.replace` method](https://docs.python.org/3/library/dataclasses.html#dataclasses.replace), which also encourages the pattern of making sure you know _where_ your data came from by explicitly storing new copies:
    ```python3
    def louden_my_pet(my_pet: Pet) -> Pet:
        return my_pet.replace(name=my_pet.name.upper() + "!!!")

    my_cat = Pet(name="Spots")
    my_loud_cat = louden_my_pet(my_cat)  # SPOTS!!! came from Spots and is distinct
    ```

Adding an equality operator and using hashable field types makes your dataclass usable in hashed containers (`dict`/`set`):

```python3
import dataclasses

@dataclasses.dataclass(eq=True, frozen=True)
class PairOfItems:
  left: str
  right: str

directed_graph_with_node_descriptions: dict[PairOfItems, str] = {
    PairOfItems(left="a", right="b"): "A to B",
    PairOfItems(left="b", right="c"): "B to C",
    PairOfItems(left="a", right="d"): "A to D",
}
```

In general, it's easier to reason about code that generates new data than it is code that mutates data. Dataclasses and type hints help enforce this.

Getting Json from a dataclass is relatively easy, assiming you have no exotic data types:

```python3
json.dumps(dataclasses.asdict(my_pet))
```

## Moving to Dataclasses from Namedtuples

There is [a typed version of `namedtuple` in the standard library](https://docs.python.org/3/library/typing.html#typing.NamedTuple) you can use, with basic usage very similar to dataclasses, as an intermediate step toward using full dataclasses (e.g. if you have code that uses tuple unpacking syntax that you can't refactor yet).

```python3
class Manifest(T.NamedTuple):
    filename: str
    xml: bytes
    records_ids: list[int]

filename, source, records_to_mark = Manifest(filename='text.xml', xml=b'<xml />', record_ids=[1, 2, 3])  # type: str, bytes, T.List[int]
```

## Additional Levels of Sophistication: Validation with Pydantic
Since type hints are just that, hints, in Python. Using dataclasses with types fields doesn't enforce types going in, nor does it do any sort of data validation. If you reach the stage where this is needed, the Pydantic library has [a drop-in replacement for dataclasses](https://pydantic-docs.helpmanual.io/usage/dataclasses/) that gives you all the type coercion and data validation pydantic offers on its native data structures. To get started, you can get pretty far with a `s/@dataclasses.dataclass/@pydantic.dataclasses.dataclass/` search-and-replace on your codebase.

You then have access to [Pydantic data validation](https://pydantic-docs.helpmanual.io/usage/validators/#dataclass-validators) as well:

```python3
@dataclasses.dataclass(frozen=True)
class LoudPet:
    name: str

    @validator('name', pre=True, always=True)
    def set_name(cls, v):
        return v.upper() + "!!!"

my_cat = LoudPet(name="Spots II: Son of Spots")
```
> `LoudPet(name='SPOTS II: SON OF SPOTS!!!')`

## Better JSON Round-Tripping for "Free" With Pydantic

We deal with APIs and our bread-and-butter is writing HTTP-based, RESTful services. This means a large part of what we do is translating data models to/from JSON as they interchange between various systems written in various languages and frameworks.

By moving to pydantic, we get type coersion in our data strcutures, so for fields that are `datetime`s or `UUID`s coming from a JSON struct (where they are usually downcast to string) it will do the right thing and coerce to those types, unlike plain dataclasses.

Pydantic also has [a default JSON encoder](https://pydantic-docs.helpmanual.io/usage/dataclasses/#json-dumping) that will attempt to do the right thing with some common datatypes (looking at `datetime` and `uuid` again). You might still need to write your own encoder to handle your own datatypes, but you can base it on pydantic's as a starting point.

```python3
from pydantic.json import pydantic_encoder

return_json: str = json.dumps(my_pet, default=pydantic_encoder)
```

# Enumerations
Related to Dataclasses are [proper enumeration support in the Python Standard Library](https://docs.python.org/3/library/enum.html).

```python3
class ManifestState(enum.Enum):
    # Standard JIT unmanifested shipment
    UNMANIFESTED = 0

    # Standard JIT manifested shipment
    MANIFESTED = 1

    # Shipment has some error to signal the manifester to ignore
    ERROR = 2
```

This means you can use `ManifestState.MANIFESTED.value` instead of a literal value, and you can group your constants into a single namespace. It also has nice validation like making sure the same constant isn't reused and adding auto-incrementing values for int values so you don't have to do it manually.

# Putting it All Together

Imagine the following set of endpoints:

| Endpoint | Function | 
| --- | --- |
| `/shipment` | Create a new shipment object |
| `/shipment/:id` | Fetch a shipment object by ID |

We can model a `Shipment`:

```python3
@dataclass
class Address:
    recipient: str
    line1: str
    line2: str | None
    zip: str | None
    city: str | None
    state: str | None
    country: str

class ShipmentState(enum.Enum):
    NEW = "New Shipment"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    RETURNED = "Returned"
    ERROR = "Error"

@dataclass
class Shipment:
   from_address: Address
   to_address: Address
   weight_in_ounces: int
   state: ShipmentState = ShipmentState.NEW
```

And then `POST` to an endpoint:

```python3
@post('/shipment')
def create_shipment(request):
    # Validation, safety, etc left as an exercise for the reader
    new_shipment = Shipment(**json.loads(request.body))
    shipment_id: uuid.UUID = database_module.create_shipment(new_shipment)

    return json.dumps({'id': shipment_id}, default=pydantic_encoder)
```

And to fetch:

```python3
from pydantic import validate_arguments

@get('/shipment/{shipment_id}')
@validate_arguments
def get_shipment(request, shipment_id: UUID):
    # 404s, authentication, etc left as an exercise for the reader
    shipment_object: Shipment = database_module.get_shipment(new_shipment)
    return json.dumps(dataclasses.asdict(shipment_object), default=pydantic_encoder)
```

# Conclusion

The Python language is still progressing and improving. Recent versions have added plenty of value, both in terms of new functionality and improved behavior on existing functionality. Using these new features can make code cleaner, easier to read, easier to be confident about, and generally less painful to maintain.