+++
title =  "Mixed Async code in Sync Python: Disappointingly Simple"
date = 2022-09-23T00:00:00-08:00
tags = ["python", "programming"]
featured_image = ""
description = "Python: Yeah."
draft = false
+++

One thing I love about Python's practical approach to type annotations and enforcement is that it's gradual: you can rapidly code a large ball of mud and get it working, then refine it to make it safer with typing later on.

Chalk this up as another cood idea (possibly by accident) for Python: you can do the same with async.

At work, someone lamented that threads aren't quite safe but they needed to do multiple http requests in parallel.

After being _that asshole_ and suggesting they rewrite the entire app as an async app , I went in an experimented for a few hours. I experimented and coded and came up with a simple, almost disappointingly so, solution:

```python
import asyncio
from unittest import FunctionTestCase

import aiohttp


async def fetch_url(session, url) -> tuple[str, str | Exception]:
    try:
        async with session.get(url) as result:
            return (url, await result.text())
    except Exception as e:
        return (url, e)


async def fetch_urls_async(*urls) -> dict[str, str]:
    async with aiohttp.Session() as session:
        return {
            url: str(status)
            for url, status in asyncio.gather(fetch_url(session, url) for url in urls)
        }


def get_multiple_urls() -> dict[str, str]:
    return asyncio.run(
        fetch_urls_async("http://www.google.com", "http://www.zombo.com")
    )


@flaskapp.route("/")
def main_sync_route():
    return get_multiple_urls()
```

The three parts to make this work:

* `async`-colored functions
* [`asyncio.gather`](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather) to run a pool of jobs
* [`asyncio.run`](https://docs.python.org/3/library/asyncio-task.html#asyncio.run) to run a block of async code in a sync context

Long story short: `asyncio.run` does exactly what it says on the tin with minimal fuss. If you're not in an async event loop in the current thread, it starts one for you, runs the async function as its main, then blocks until it's done.