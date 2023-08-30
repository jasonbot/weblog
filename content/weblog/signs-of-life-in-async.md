+++
title =  "Registering Signs of Life in Long-Running Async Jobs in Python"
date = 2023-08-13T00:00:00-08:00
tags = ["python", "programming"]
featured_image = ""
description = ""
+++

At work I'm currently working on a fairly large system in which we have a pool of greedy workers, of unknown size, which can opt it at any time to the flow of work.

A job is considered abandoned if it is marked as `IN_PROGRESS` but the worker who has claimed it hasn't phoned home in sone amount of time.

The project is async, which makes things bot more and less interesting. It looks something like this:

```python
@contextlib.contextmanager
def run_keepalive_function_while_awaiting(
    call: typing.Callable[[None], typing.Awaitable[None]], interval: float = 1.0
):
    alive = True

    async def _keepalive():
        while alive:
            await call()
            await asyncio.sleep(interval)

    asyncio.create_task(_keepalive(), name=f"Keepalive task utilizing {call}")

    yield

    alive = False
```

And then basic usage is like this:

```python
async def do_the_work():
    job_id = uuid.uuid4()

    async def announce_signs_of_life():
        responses.post("http://job-scheduler/i-am-alive/{job_id}")

    with run_keepalive_function_while_awaiting(announce_signs_of_life, 0.25):
        await do_long_running_task()
```

As long as the code block in the `run_keepalive_function_while_awaiting` context manager is running, the system will run a background coroutine that periodically runs the keepalive function.
