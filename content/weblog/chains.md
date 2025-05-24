+++
title = "Chains: My Attempt at an Itertools for Go"
date = 2025-05-24T00:00:00-08:00
tags = ["golang", "programming"]
featured_image = ""
description = "Here I Go (this is a pun and I regret it immediately)"
+++

> **Top Matter**: [Github for the library](https://github.com/jasonbot/chains), [doc for the library](https://pkg.go.dev/github.com/jasonbot/chains).

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

Once I had a framework cooking I could start thinking of examples. [My test suite took a backdoor to being a test of cases I cared about](https://github.com/jasonbot/chains/blob/main/cookbook_test.go), in cookbook form.

Some things I wanted:

- Map/Filter/Reduce
- Cleanups (compacts, nonzeroes, etc)
- Combinatorics
- Higher-level stream processing (various merges)

## Map/Filter/Reduce

Not much to write home about here, anyone can write these and I encourage each person to do it themselves using Go iterators.

## Cleanups

Similar to the above, pretty trivial to write. Can even treat these as specific cases of `Filter`.

## Combinatorics

I wanted `combinations` and `permutations`, so those were high on the list. I found myself writing the code more and more generically as I went along, eventually ending with the mess that is [`combinatorics.go`](https://github.com/jasonbot/chains/blob/main/combinatorics.go). Funnily enough, each combinatorial case was some combination of:

- Length (one, fixed, variable)
- Ordering (in order of occurrence, free variance)
- Repetition of elements (on/off)

| Function                              | Length                   | Ordering | Repetition |
| ------------------------------------- | ------------------------ | -------- | ---------- |
| (Identity function, superfluous)      | N (Length of inputs)     | Fixed    | No         |
| `OrderedPermutations`                 | 1...N (Length of inputs) | Fixed    | No         |
| `OrderedPermutationsOfLength`         | M (User-specified)       | Fixed    | No         |
| `AllPermutations`                     | 1...N (Length of inputs) | Free     | No         |
| `Permutations`                        | N (Length of inputs)     | Free     | No         |
| `PermutationsOfLength`                | M (User-specified)       | Free     | No         |
| `PermutationsWithReplacement`         | N (Length of inputs)     | Free     | Yes        |
| `PermutationsOfLengthWithReplacement` | M (User-specified)       | Free     | Yes        |
| `Combinations`                        | 1...N (Length of inputs) | Free     | Yes        |
| `CombinationsOfLength`                | 1...M (User-specified)   | Free     | Yes        |

## Windows

Not as high-level as Combinatorics, but I wanted to take a window of N at as time.

| Function         | Length | Overlaps | Examples                              |
| ---------------- | ------ | -------- | ------------------------------------- |
| `Windows`        | 1...M  | No       | `{1, 2, 3}, 2 -> {1, 2}, {3}`         |
| `SlidingWindows` | 1...M  | Yes      | `{1, 2, 3}, 2 -> {1, 2}, {2, 3}, {3}` |

## Higher-Level Chaining

I like to concatenate iterators sometimes; e.g. to process the results of two tasks in a single queue. `itertools.chain` works in Python, it was a breeze to write here as well.

```go
for x := range chains.FlattenArgs(chains.Each([]int{1, 2, 3}, []int{4, 5, 6})) {
    /// Gives you 1, 2, 3, 4, 5, 6
}
```

Got the base case down.

## Things I Never Had in Itertools: Merging Iterators

Some common use cases I find myself writing a lot just aren't in the stdlib in Python. They generally involve taking many iterators and unifying then in ways dependent on the structure of the iterators themselves; either by length or by value.

### Combining Streams "Fairly"

Another use case is Round-Robining a set of iterators until they are all exhausted. We've got a set of inputs and want to consume from all of them until we run out. For that, there's [`RoundRobin`](https://github.com/jasonbot/chains/blob/main/cookbook_test.go#L261-L272), which works exactly as expected. Each iterator can have a variable number of entries but all entries are considered by index, so we don't exhaust one before going to the next but try to consume them all equally.

```go
item1 := []int{1, 2, 3, 4}
item2 := []int{5, 6, 7, 8}
item3 := []int{9, 10, 11, 12}

for x := range RoundRobin(Each(item1), Each(item2), Each(item3)) {
    // Equivalent of ...[]int{1, 5, 9, 2, 6, 10, 3, 7, 11, 4, 8, 12}
}
```

### Merging Sorted Streams

Use case: I have 3000 CSVs, each has rows in order of date. The time ranges _may_ overlap in some cases. I wanted a unified stream of all the rows in order. For that, I wrote [`Merged`](https://github.com/jasonbot/chains/blob/main/cookbook_test.go#L231-L259), which is at its core a pull-on-demand heap. Once the smallest value has been pulled off, pull another item from the iterator to got that item from and put it back on the heap.

```go
item1 := []int{1, 2, 3, 4}
item2 := []int{4, 5, 6, 7}
item3 := []int{1, 5, 8, 10}

expectedSlice := []int{1, 1, 2, 3, 4, 4, 5, 5, 6, 7, 8, 10}
for x := range Merged(Each(item1), Each(item2), Each(item3)) {
    // Equivalent of ...[]int{1, 1, 2, 3, 4, 4, 5, 5, 6, 7, 8, 10}
}
```

# My Journey of Discovery got me Using My Favored Pattern in a More Go-Like Way in Go

I was in love with my ability to do chained iterators, but they got clunky. Go generics only apply to functions and you can't template an interface. So while `X.Filter(...).Map(...)` is fun and cute, in Go you're better off doing something like:

```go
f := Filter(X, filterFunc)
m := Map(f, mapfunc)

for results := range m {...}
```

...which, quite frankly, feels a lot more Go-like and less foreign than the cute way we do it in other languages. You can see I gave up on chaining in the above examples and just do individual iterators.

Once I started doing things the Go way, it really increased the pace of development as well. Being able to implement each iterator as a simple function meant I could focus on implementation and not boilerplate. Constraining myself to `iter.Seq` and `iter.Seq2` relieved me of the analysis paralysis of variadic iterators: one value, and when it made sense, two.

# Don't Use this as a Library

I've made this available as an importable library, but many of these patterns are easier to just copy and paste into your code. They should also be inspiration: this is a fun problem to solve! Solve it yourself!
