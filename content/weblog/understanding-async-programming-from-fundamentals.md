+++
title =  "Async programming: understanding it from fundamentals"
date = 2022-07-12T00:00:00-00:00
tags = ["programming", "python", "javascript"]
featured_image = ""
description = "It's simpler when you build up your knowledge from a base"
+++

> This was inspired by a short chat I had with a coworker, trying to give a simple, 15 minute explanation of something that took me a decade to wrap my head around due to poor teaching resources online.

Async programming in modern "industrial" languages is shrouded in magic, abstractions, and years of atrocious decisions (looking at you, Javascript/Python). Most tutorials start out with "just mark your function `async` and `await` it and use these magic incantations and you're good to go!" without explaining the underlying concepts that were built up

## Async is (mostly) only good for things with long, unpredictable waits

What has long, unpredictable wait times? Anything I/O bound, _especially_ network traffic. CPU bound tasks were solved long ago with several approaches, namely threading and SIMD instruction data sets. I/O can still bring a multithreaded application to its knees.

Based on this, threading on its own isn't _necessarily_ the best way to approach this, or at least, not polling by spawning one thread per open connection. With a single-threaded approach, at least for the I/O part, how would we go about it? IT probably makes sense to have a blocking call on not just one socket, but _many_.
That is, instead of `socket.wait()` we could call `[socket1, socket2, ...].wait()`. Note we could already discount something with a `.ready()` poll instead of a `.wait()` because

```python3
while True:
    s = [socket for socket in sockets if socket.ready_to_read()]
```

would thrash the CPU and turn the server into a space heater. A block would be better.

## `select`: The great granddaddy of async programming

In general, with I/O bound programs, you'd probably want to avoid spawning a thread for every request because that's pretty hard on the OS kernel and not particularly scalable. If you could _move_ all those waiting-on-input blocks to the kernel, where it should live, that would help.

So in theory, if you listen to a list of open network sockets, you want to just block and get a list of handles with data ready to go. In Python pseudocode:

```python3
while True:
    for socket in magic_handler(list_of_sockets)
        handle_data_ready(socket.id, socket.read())
```

Or to expand more closely to "working" code:

```python3
# The open TCP socket accepting connections
listener = socket.listen()
sockets = [listener]
handlers = {}

# Loop until loop is broken
while True:
    # Handles to close this iteration
    closed_handle_ids = set()
    handles = magic_listener(sockets)

    # Go over currently ready-to-read connections
    for handle in handles:
        # Is this the listening socket?
        if handle.id == listener.id:
            # Get the actual connection we just established from the listener
            new_handle = handles.append(handle.accept())
            sockets.add(new_handle)
            handlers = ConnectionHandler(handle)
        # Is this a request handler?
        else:
            # Feed the handler the data ready
            handlers[handle.id].handle_data(handle.read())

        # Is this handle done with its request?
        if handle.done:
            closed_handle_ids.append(handle.id)
            handlers[handle.id].close()
            del handlers[handle.id]

            # Done listening (this is the special listener socket)
            if handle.id == listener.id:
                break

    # Delete active handles
    sockets = [s for s in sockets if s.id not in closed_handle_ids]
```

You can see this is already getting scary just looking at basic cases without error handling. You probably don't want to roll this code on your own.

So there's the original Posix function `select`:

```c
int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *errorfds, struct timeval *timeout);
```

It's even more complex than the code above in that it handles read/write/error states, but the main concept is still clearly there: a blocking call that returns list of handles for read/write when they are ready.

### Moving on

From this basic understanding, you can intuit that 1) there are probably a lot of corner cases to debug and 2) there is probably a better way to do it.

And from here you now understand 1) the need for the amorphous "event loop" provided by a third-party library that has gone through the long process of fishing out edge cases and bugs so you don't have to and 2) the evolution of new APIs like `epoll` and `kqueue` that do the same thing, but better. And, as a bonus, a combination of both in abstraction libraries like `libevent`.

## "Cooperative" multitasking and event loops

This is a problem as old as time. Even on older desktop frameworks like Classic Mac OS and Windows the default for applications was by design to run in a single-threaded event loop and the program is expected yield to the operating system periodically so it could do housekeeping tasks and let other running apps run for a slice of time too.

Lots of software are bad citizens. Doing CPU intensive work in this type of framework will inevitably not yield to the loop at a reasonable clip and cause the entire system to become unresponsive. This can still hit you with asynchronous apps today.

## We need a scheduler

On a higher level, especially in interpreted languages, it's possible during code execution to say "this item has used _N_ opcodes, let's pump the brakes a second." This has the potential in the event loop to make long running code that does not yield not hang the whole system and also lets you transparently spin off subtasks ("green threads") with impunity from your function and be able to trust they will run.

## The iterator protocol in Python and "cooperative" multitasking

In Python, you can make a function a _generator_ by using the `yield` keyword at least once. You then run the function by calling it with arguments, which in turn returns a generator, which you can use the `next()` builtin on or use in a `for` loop.

This gives us a framework for "cooperative" multitasking. Consider this:

```python3
generators = []

def add_task(generator):
    generators.append(generator)

def task(generation=0):
   print(f"Hello from generation {generation}")
   yield
   if generation < 100:
        (f"Adding task from generation {generation}")
        add_task(generation+1)
   yield
   print((f"Generation {generation} is done"))
   return generation


def event_loop(start_generator):
    generators.append(start_generator)
    while generators:
        generator = generators.pop(0)
        try:
            next(generator)
            # Push "coroutine" to end of task list
            generators.append(generator)
        except StopIteration as e:
            print(f"Generator finished and returned {e.value}")

# Start the "event loop" with a single root task.
event_loop(task())
```

This code takes a generator, iterates over it until it's done, and also allows it to add new subtasks to the cooperative job runner. Now you've got an interpreter-level event loop; the event loop could be smarter and look at each `yield`s yield value, and if it's a filehandle etc the even loop could take that, squirrel it away into a list of handles being waited on, and not add the generator back into the queue until a `select` call says that handle is ready for reading again. I.E. `yield handle.read()` where `handle.read()` sends off some sort of object with a file handle ID to the scheduler and then the event loop does a `.send()` with the data ready to be read so you could do `data = yield handle.read()` and have the event loop be able to push your coroutine aside in an efficient way until it's ready to go again. This also lets you do other blocking calls like `time.sleep()` in a cooperative manner, too.

That is, making our own "cooperative" event loop based on iterators makes it possible to make otherwise blocking calls non-blocking to cooperating green threads, delegating the long wait to the event loop and also making it possible to spawn new green threads within that event loop.

## Promises

One concept of industrial async applications is the concept of a _Promise_: a function will return a _Promise_ rather than an actual return value, and shove off its workload using something approximating the above iterator to the event loop.

A promise is an cooperatively async way of doing this:

```python3
def promise(fn, then, error):
    try:
        val = fn()
        then(val)
    except Exception as e:
        error(e)
```

However, it's fairly ugly in practice in Javascript and is a lot more jarring to write a pyramid of `.then()` calls to do sequential code. This is what most Javascript in the wild does; but it's jarring and it would be nicer to get a syntax closer to the above with `yield`.

## `async` and `await`: Syntactic and semantic sugar on Promises

As we discussed above, with an interpreted language we can easily implement in our runtime an implicit event loop and a forced "cooperative" mode that can pause code after a certain number of opcodes.

Many languages (Python/Javascript/C#/etc) have introduced the `async` and `await` keywords, all semantically similar. Marking a function as `async` informs the interpreter/runtime that this function will span cooperative "subtasks" and need to be put into consideration for the event loop's scheduler.

The `await` keyword says "push this async function onto the list of green threads and call me back when it finishes/errors with the result." It pauses the function that `await`s and doesn't put it back into the stack until the dependent green thread returns or fails, and then pushes the paused coroutine into the list of active green threads and sends it the return value.

## The problem

Async code _can still block_ if it calls synchronous functions, and you have to keep track of what code _is_ and _isn't_ async, avoiding mixing the two. Python, by nature of having an event loop at the interpreter level, is more susceptible to this than Javascript, but you still need to take care not to call long-running non-async functions from async code.

## Conclusion

I hope this helps build up from fundamentals the basics of how async programming works in modern systems.

## Further Reading

- [What color is your function?](https://journal.stuffwithstuff.com/2015/02/01/what-color-is-your-function/)
- [Python `yield`](https://docs.python.org/3/reference/expressions.html#yieldexpr)
- [Coroutines via enhanced iterators](https://peps.python.org/pep-0342/)
- [Python Coroutines with `async` and `await` Syntax](https://peps.python.org/pep-0492/)
- [Javascript Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [Javascript `await`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/await)
