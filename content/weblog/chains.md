+++
title = "Chains: My Attempt at an Itertools for Go"
date = 2025-05-24T00:00:00-08:00
tags = ["golang", "programming"]
featured_image = ""
description = "Here I Go (this is a pun and I regret it immediately)"
+++

> **Top Matter**: [GitHub for the library](https://github.com/jasonbot/chains), [doc for the library](https://pkg.go.dev/github.com/jasonbot/chains).

It's been six months since I've done this, but I'm finally writing about it!

Go [recently added proper iterator support](https://go.dev/blog/range-functions) to the language, which is something of an improvement over the prior pattern of spinning up a goroutine and communicating via a channel in a `range` to get a stream of values.

One of the tools in my toolbox that I use in coding interviews and some light data processing work is [Python's itertools](https://docs.python.org/3/library/itertools.html). The nice thing about this library is it gives you a good set of conceptual building blocks to use as a frame around a problem and a fairly clean way to use them. Once you're familiar with, say, `combinations` and `permutations` you can take a harder problem and decompose it into those recognizable parts and then have a stdlib function that's already bug free and readily available.

While I was inspired to author this, I was writing a _lot_ of Ruby and Typescript. Both Ruby and Javascript do processing over lists in a very chainy way; for example

```javascript
Object.entries(thing)
  .filter(([key, value]) => key.startsWith("data-"))
  .map(([key, value]) => `${key.replace(/^data-/, "")}: ${value}`);
```

Ruby likes to add lots of [compact](https://docs.ruby-lang.org/en/2.5.0/Array.html#method-i-compact) calls etc. as well to handle bad data.

Having this syntactic sugar makes it easier to write complex logic, and it also helps conform the logic to one's brain.

Anyway, Go has iterators now, and I like using iterators. The first thing I wanted was my brain poisoning syntactic sugar from Ruby/Typescript; how could I go about doing `X.Filter(g => g > 100).Map(h => fmt.Sprintf("Hello, %v!", h))` in Go?

# The Cookbook is the Requirements Doc

Once I had a framework cooking I could start thinking of examples. [My test suite took a backseat to being a test of cases I cared about](https://github.com/jasonbot/chains/blob/main/cookbook_test.go), in cookbook form.

Some things I wanted:

- Map/Filter/Reduce
- Cleanups (compacts, nonzeroes, etc)
- Combinatorics
- Higher-level stream processing (various merges)

## Map/Filter/Reduce

Not much to write home about here, anyone can write these and I encourage each person to do it themselves using Go iterators. There's the usual suspects here along with various types of `Reduce` that all boil down to the base [`Accumulate`](https://pkg.go.dev/github.com/jasonbot/chains#Accumulate).

## Cleanups

Similar to the above, pretty trivial to write. Can even treat these as specific cases of `Filter`. [`Compact` is one such case](https://pkg.go.dev/github.com/jasonbot/chains#Compact).

## Basic Tests

- There's an `Any` and an `All` for testing for conditions satisfied by the entire sequence; `Count` gets just the length. All are useful with `Tee`!

## Slicing

- `First` and `Last` do what they say; `FirstAndRest` is the CAR/CDR you didn't know you needed.
- You can `TakeWhile` and `DropUntil` to start/end at a particular point.
- You can `Repeat` an item N times, `Rotate` a slice so the first N items are moved to the back, `Repeat` each element N times, and `Cycle` the iterator which is just infinite repeats.

## Ruby Silliness

- [`Flatten` takes an iterable of iterables and turns it into a flat iterable](https://pkg.go.dev/github.com/jasonbot/chains#Flatten), but it doesn't do it to arbitrary levels of nesting like Ruby does. There are rules here dude.
- [`Tap` is largely useless](https://pkg.go.dev/github.com/jasonbot/chains#Tap), kind of like a forEach or a visitor that passes the item along.
- [`Partition` splits an iterator into two](https://pkg.go.dev/github.com/jasonbot/chains#Partition) based on a partition function, allowing you to e.g. split good/bad inputs into separate pipelines. A simpler [`Uniq`](https://pkg.go.dev/github.com/jasonbot/chains#Uniq) function just returns the first value of each key grouping instead.
- Similarly, [`GroupBy`](https://pkg.go.dev/github.com/jasonbot/chains#GroupBy) takes an ordered set of items and "bins" them based on a key function, allowing you to `for key, vals := range Partition { for val := range vals { ...} }`
- There's also a `Tee` to get a tear-off copy of the iterator.

## Combinatorics

I wanted `combinations` and `permutations`, so those were high on the list. I found myself writing the code more and more generically as I went along, eventually ending with the mess that is [`combinatorics.go`](https://github.com/jasonbot/chains/blob/main/combinatorics.go). Funnily enough, each combinatorial case was some combination of:

- Length (one, fixed, variable)
- Ordering (in order of occurrence, free variance)
- Repetition of elements (on/off)

| Function                         | Length                   | Ordering | Repetition |
| -------------------------------- | ------------------------ | :------: | :--------: |
| (Identity function, superfluous) | N (Length of inputs)     |  Fixed   |     No     |
| `OrderedPermutationsOfLength`    | M (User-specified)       |  Fixed   |     No     |
| `AllOrderedPermutations`         | 1...N (Length of inputs) |  Fixed   |     No     |
| `OrderedPermutationsToLength`    | 1...M (User-specified)   |  Fixed   |     No     |
| `Permutations`                   | N (Length of inputs)     |   Free   |     No     |
| `PermutationsOfLength`           | M (User-specified)       |   Free   |     No     |
| `AllPermutations`                | 1...N (Length of inputs) |   Free   |     No     |
| `PermutationsToLength`           | 1...M (User-specified)   |   Free   |     No     |
| `Combinations`                   | N (Length of inputs)     |   Free   |    Yes     |
| `CombinationsOfLength`           | M (User-specified)       |   Free   |    Yes     |
| `AllCombinations`                | 1...N (Length of inputs) |   Free   |    Yes     |
| `CombinationsToLength`           | 1...M (User-specified)   |   Free   |    Yes     |

## Windows

Not as high-level as Combinatorics, but I wanted to take a window of N at as time.

| Function         | Length | Overlaps | Examples                         |
| ---------------- | :----: | :------: | -------------------------------- |
| `Windows`        | 1...M  |    No    | `{1, 2, 3}, 2 -> {1, 2}, {3}`    |
| `SlidingWindows` |   M    |   Yes    | `{1, 2, 3}, 2 -> {1, 2}, {2, 3}` |

## Higher-Level Chaining

I like to concatenate iterators sometimes; e.g. to process the results of two tasks in a single queue. `itertools.chain` works in Python, it was a breeze to write here as well.

```go
for x := range chains.FlattenArgs(chains.Each([]int{1, 2, 3}, []int{4, 5, 6})) {
    /// Gives you 1, 2, 3, 4, 5, 6
}
```

Got the base case down.

## Things I Never Had in Itertools: Merging Iterators

[`itertools.chain` works in a pinch for "gluing" together iterators in Python](https://docs.python.org/3/library/itertools.html#itertools.chain), and that was pretty trivial to write ([I called it "Flatten"](https://pkg.go.dev/github.com/jasonbot/chains#Flatten) because the first iteration took an iterator of iterators, thanks to Ruby/Javascript brain, [then made one that took variadic iterator args as `FlattenArgs`](https://pkg.go.dev/github.com/jasonbot/chains#FlattenArgs) too). Some common use cases I find myself writing a lot just aren't in the stdlib in Python. They generally involve taking many iterators and unifying then in ways dependent on the structure of the iterators themselves; either by length or by value.

### Combining Streams "Fairly"

Another use case is Round-Robining a set of iterators until they are all exhausted. We've got a set of inputs and want to consume from all of them until we run out. For that, there's [`RoundRobin`](https://github.com/jasonbot/chains/blob/main/cookbook_test.go#L261-L272), which works exactly as expected. Each iterator can have a variable number of entries but all entries are considered by index, so we don't exhaust one before going to the next but try to consume them all equally.

```go
item1 := []int{1, 2, 3, 4}
item2 := []int{5, 6, 7, 8, 9}
item3 := []int{10, 11, 12}

for x := range RoundRobin(Each(item1), Each(item2), Each(item3)) {
    // Equivalent of ...[]int{1, 5, 10, 2, 6, 11, 3, 7, 12, 4, 8, 9}
}
```

### Merging Sorted Streams

Use case: I have 3000 CSVs, each has rows in order of date. The time ranges _may_ overlap in some cases. I wanted a unified stream of all the rows in order. For that, I wrote [`Merged`](https://github.com/jasonbot/chains/blob/main/cookbook_test.go#L231-L259), which is at its core a pull-on-demand heap. Once the smallest value has been pulled off the heap, yield it, then grab the next value from the iterator that provided the value to place on the heap.

```go
item1 := []int{1, 2, 3, 4}
item2 := []int{4, 5, 6, 7}
item3 := []int{1, 5, 8, 10}

expectedSlice := []int{1, 1, 2, 3, 4, 4, 5, 5, 6, 7, 8, 10}
for x := range Merged(Each(item1), Each(item2), Each(item3)) {
    // Equivalent of ...[]int{1, 1, 2, 3, 4, 4, 5, 5, 6, 7, 8, 10}
}
```

# My Journey Of Discovery Got Me Using My Favored Pattern In A More Go-Like Way In Go

## Starting Out: The `Chain`

I wanted to be able to chain calls like I can in _those other_ languages, so the first thing I thought to do was design some sort of struct or interface with various `.Map`/`.Reduce`/`.Filter`/etc methods -- so like

```go
type Chainable interface {
    Map(mapFunc(T) V) Chainable[V]
    Reduce(mapFunc(T) V) Chainable[V]
    Filter(mapFunc(T) V) Chainable[V]
}
```

Immediately there's a problem because Interfaces can't use generics in Go, so we do a struct instead:

```go
type Chainable[T] struct {
    func(c *Chainable) Map(mapFunc(T) V) Chainable[V] { ... }
    Reduce(mapFunc(T) V) Chainable[V] Chainable[V] { ... }
    Filter(mapFunc(T) V) Chainable[T] Chainable[V] { ... }
}
```

This sort of works! You can see in the [`IterableSequence` type ](https://pkg.go.dev/github.com/jasonbot/chains#IterableSequence) we do this. But to do two types (say we're mapping from `int` to `string`), we have to have an `IterableSequence` that does two, and so [`IterableSequence2` was born](https://pkg.go.dev/github.com/jasonbot/chains#IterableSequence2).

Now how to get from an `IterableSequence` to an `IterableSequence2`? I decided on a top-level function to create [a type called a `Junction`](https://pkg.go.dev/github.com/jasonbot/chains#ChainJunction) to go from a one-typed chainable to a two-typed one. Now what if we need a third type? This is getting messy.

This pattern works for simple cases just fine, but it falls down once we get into the variadic world. Go's obviously stunted-on-purpose generics are preventing us from doing this syntactic sugar in a clean way, but it is also suggesting a different way to do it.

I was in love with my ability to do chained iterators, but they got clunky. Go generics only apply to functions and you can't template an interface. So while `X.Filter(...).Map(...)` is fun and cute, in Go you're better off doing something like:

```go
f := Filter(X, filterFunc)
m := Map(f, mapfunc)

for results := range m {...}
```

...which, quite frankly, feels a lot more Go-like and less foreign than the cute way we do it in other languages. You can see I gave up on chaining in the above examples and just do individual iterators.

And so, instead I found myself using single iterators via [the `Each` adapter function](https://pkg.go.dev/github.com/jasonbot/chains#Each) and back to slices [with `ToSlice`](https://pkg.go.dev/github.com/jasonbot/chains#ToSlice). As I got further into implementing the various functions I wanted, I moved away from the `Chainable` pattern into simple functions. It's still ugly to do `Map(Filter(Reduce(...)))` because the pipeline appears in opposite order but doing each as an assignment keeps the order at the expense of slightly more verbosity. It's not as _aesthetic_ but it works.

I think the most practical example I can give is the test in the cookbook that generates a sequence of fights in Street Fighter. If you play as a playable character you can fight all the other playable characters _and_ each of the bosses. You _cannot_ play as the bosses. As such, we have two separate matchup types:

- Player v Player, unordered
- Player v Boss, unordered

And gluing the two together is pretty clean:

```go
regularFighters := []string{"Ryu", "Chun Li", "Guile", "E. Honda"}
bosses := []string{"Sagat", "Vega", "M. Bison"}

allExpectedFights := []string{
    "Ryu vs. Chun Li",
    "Ryu vs. Guile",
    "Ryu vs. E. Honda",
    "Chun Li vs. Guile",
    "Chun Li vs. E. Honda",
    "Guile vs. E. Honda",
    "Ryu vs. Sagat",
    "Chun Li vs. Sagat",
    "Guile vs. Sagat",
    "E. Honda vs. Sagat",
    "Ryu vs. Vega",
    "Chun Li vs. Vega",
    "Guile vs. Vega",
    "E. Honda vs. Vega",
    "Ryu vs. M. Bison",
    "Chun Li vs. M. Bison",
    "Guile vs. M. Bison",
    "E. Honda vs. M. Bison",
}

// Each combination of players without replacement
matchups := CombinationsOfLength(regularFighters, 2)
singlePlayerFights := Map(matchups, func(names []string) string {
    return strings.Join(names, " vs. ")
})

// Trick to get pairwise fights from two lists -- lengthen the one by
// the number of elements in the other, then cycle.
// e.g. if you have P1, P2, P3 and B1, B2:
// Cycle --> P1, P2, P3, P1, P2, P3, P1, ...
// Lengthen --> B1, B1, B1, B2, B2, B2
//      (each boss is repeated number of players times)
bossMatchups := Zip(
    Cycle(Each(regularFighters)),
    Lengthen(
        Each(bosses),
        len(regularFighters),
    ),
)

bossMatchupFights := Map2(bossMatchups,
    func(p1, p2 string) string {
        return strings.Join([]string{p1, p2}, " vs. ")
    },
)

// Combine all iterators into one
allFightsCombined := FlattenArgs(singlePlayerFights, bossMatchupFights)
allFights := ToSlice(allFightsCombined)

if !slices.Equal(allFights, allExpectedFights) {
    t.Fatalf("%v != %v", allFights, allExpectedFights)
}
```

Once I started doing things the Go way, it really increased the pace of development as well. Being able to implement each iterator as a simple function meant I could focus on implementation and not boilerplate. Constraining myself to `iter.Seq` and `iter.Seq2` relieved me of the analysis paralysis of variadic iterators: one value, and when it made sense, two.

# Don't Use This As A Library

I've made this available as an importable library, but many of these patterns are easier to just copy and paste into your code. They should also be inspiration: this is a fun problem to solve! Solve it yourself!
