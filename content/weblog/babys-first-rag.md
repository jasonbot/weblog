+++
title =  "A (Mostly) Practical Guide to Self-Hosting a RAG"
date = 2024-07-01T00:00:00-08:00
tags = ["programming", "llm"]
featured_image = ""
description = ""
+++

{{< toc >}}

# Introduction

As an exercise in self-improvement and understanding what the hell it is I actually do at work, I had promised myself (and, unfortunately, my manager) I'd implement a RAG from conception to finish by Valentine's Day, 2024. It is now Independence Day weekend 2024. Missed the mark by a bit.

This post is meant to go from conception to reality in implementing a RAG on a local computer.

## Goals

What I intend for this post to be:

1. **Practical**: Actually do something useful.
1. **Educational**: I didn't know any of this stuff. If you don't know this stuff and you have a mildly overlapping skillset/world view with me, I want you, too, to hold this knowledge.
1. **Lucid and Concrete**: Minimize abstractions, give code that works and explanations that are not so generic that they hold no meaning.
1. **Self-Hosted**: This is the _absolute most important thing here_: I don't want my software doing random-ass network hops when it doesn't need to. I don't want my workflow to suddenly stop working because my trial period on service X ended. I don't want surprises on my credit card bill if I open an account with some service and do too many requests. I don't want my information leaking. I have a middling-quality gaming desktop from Costco and I want to take advantage of that sweet sweet middlest-level hardware that August 2020 had to offer.

## Anti-Goals

And what I plan for it _not_ to be:

1. **Commercially viable**: See the choice of corpus to build this on. I don't want this to provide an immediate, bundled up piece of productizable code that someone can build a business on without my knowledge. This is the same reason I don't share the source for my video games: someone will take them, plop some ads on them, and resell them on mobile devices. Or do something even worse.
1. **Turnkey**: See the above point. I don't want this to be without speed bumps and be just a single command to get up and running locally. See the above point for my reasoning. If this could be "just for fun" I'd make it easier to do.

# Retrieval-Augmented Generation

## What The Hell is a RAG?

This is super vague, and was the hardest thing to get a simple answer for.

A typical [vague-as-hell explanation](https://en.wikipedia.org/wiki/Prompt_engineering#Retrieval-augmented_generation):

> Retrieval-Augmented Generation (RAG) is a two-phase process involving document retrieval and answer formulation by a Large Language Model (LLM). The initial phase utilizes dense embeddings to retrieve documents. This retrieval can be based on a variety of database formats depending on the use case, such as a vector database, summary index, tree index, or keyword table index.

I understand all those words, but in practical terms, what exactly does that mean? Like, specifically?

## What does this mean?

Turns out, **a RAG is just a dirty trick decorated with academic language to seem less dirty to outsiders**. The long and short of it is the RAG injects extra contextual information into the chatbot to give it more domain-specificity.

For example, if you were to ask your LLM

```
What is X?
```

A RAG just does some injection tricks so the answer has some extra smarts regarding some extra information at hand. What it provides the LLM is not a raw version of your question `What is X?`, but instead:

```
Given the following information:
<Some information retrieved from another system>

How would you answer the following question:
What is X?
```

That's it. It's prompt injection with a pretty name. The injection technique may vary in sophistication, but this is what it ultimately boils down to.

# Case Study: _The Dumbest Possible Person in the Room_

On the subject of the goal of _non-commercial viability_ and my love of making the world worse, not better, I present what I wish to do with a RAG here: take the transcripts of the [Joe Rogan show](https://spoti.fi/JoeRoganExperience) and turn a chatbot into a poorly-informed, blubbering idiot.

And so is born _The Dumbest Possible Person in the Room_: a conspiracy theory addled, misinformed LLM chat that will serve to both enrage you and make you dumber at the same time.

# Getting the Data

The first step to doing the RAG is to collect the actual data. I found [this sketch-ass website with transcripts of previous Joe Rogan episodes](https://www.happyscribe.com/public/the-joe-rogan-experience), so what I want to do is take that information, extract just the stuff I care about, and index it in a form I can pull from in later steps.

## A Eulogy for `wget`

The [wget project](https://www.gnu.org/software/wget/) has been my constant companion since the early 2000s. `wget -r -l 2 http://somesite/` would quickly and reliably spider a web site two links deep. However, with modern sites (and abominations like [SPAs](https://developer.mozilla.org/en-US/docs/Glossary/SPA)) the HTML the client fetches is not the document tree that is ultimately established in the browser. So many pages

## Enter Playwright

[Selenium](https://www.selenium.dev/) came out many years ago for doing browser testing and I never really liked it -- it seemed unstable and finicky. A few generations later, we get a beautiful tool in the form of [Playwright](https://playwright.dev/), which gives us so much: Javascript and Python APIs, and simulation of multiple browsers, including the Chromium family and Firefox. It's really slick.

## Our Playwright Script

I'm going to start out by scoping out what I want to do:

1. Start at the first index page,
1. Find all the links to transcript pages on the index page,
1. Download the transcript pages,
1. Process the transcript data and place it in a database,
1. Hit "next" until there is no next button, going back to the find links step.

So to get a base script going, I'm going to ask Playwright to do a recording for me:

```shell
playwright codegen --browser chromium --target python-async --output spider.py https://www.happyscribe.com/public/the-joe-rogan-experience
```

I'm just going to click the "Next" button at the bottom of the page and stop recording. This gives me:

```python
import asyncio
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.happyscribe.com/public/the-joe-rogan-experience")
    await page.get_by_role("link", name="Next ›").click()
    await page.close()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
```

Now I want to keep clicking next until I run out of Next buttons, so I modify part of the script as follows:

```python
# All the pages to look for transcript links on
page_urls = []
try:
    while True:
        page_urls.append(page.url)
        # Try to click next, but give up if there is no button on
        # the DOM within a few seconds
        async with asyncio.timeout(2):
            await page.get_by_role("link", name="Next ›").click()
except TimeoutError:
    print("Ran out of pages to click")
finally:
    await page.close()
```

Now I'm going to look into the DOM tree to figure out the links to the transcripts:

![DOM inspector](/images/babys-first-rag/dom-inspector.png)

With this we see that the links to transcript pages all have the class `hsp-card-episode`, so we can use Javascript to find them all on the page:

```python
links = await page.evaluate(
    'Array.from(document.getElementsByClassName("hsp-card-episode")).map(a => a.href)'
)
```

We can then use this list of links to download individual pages:

```python
async def get_transcript_files(playwright: Playwright, urls: list[str]):
    download_path = pathlib.Path("./transcript_pages")
    download_path.mkdir(exist_ok=True)

    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    for transcript_page_url in urls:
        print(transcript_page_url)
        await page.goto(transcript_page_url)

        filename = f"{transcript_page_url.split("/")[-1]}.html"
        print(f"Downloading {filename}")
        with open(download_path / filename, "w") as out_handle:
            out_handle.write(await page.content())
```

# Cleaning Up the Data

At this point I have the raw HTML, and I want to extract just the parts that are interesting into a JSON file I can import into SQLite for later manipulation.

## Install Unstructured

I'm going to use a hosted instance of [the Unstructured API](https://github.com/Unstructured-IO/unstructured-api) in Docker. Unstructured is probably the best and most widely used tool for the job.

```shell
# Grab image
docker pull downloads.unstructured.io/unstructured-io/unstructured-api:latest
# Run on port 5435 just because it's not commonly used and 8000 is
docker run -p 5435:8000 -d --rm --name unstructured-api downloads.unstructured.io/unstructured-io/unstructured-api:latest
# Should return {"healthcheck":"HEALTHCHECK STATUS: EVERYTHING OK!"}%
curl http://localhost:5435/healthcheck
```

Unstructured is also my employer, so they have an incredible team of attractive geniuses working for them and it's a good idea to buy as many commercial licenses as your employer can afford when you get back to work next.

## Processing the HTML into Something More Usable

We can iterate through the downloaded HTML using [the Unstructured Python API client](https://github.com/Unstructured-IO/unstructured-python-client):

```python
in_path = pathlib.Path("./transcript_pages")
out_path = pathlib.Path("./processed_pages")
out_path.mkdir(exist_ok=True)

s = unstructured_client.UnstructuredClient(
    api_key_auth=None, server_url="http://localhost:5435/general/v0/"
)

for file in in_path.glob("*.html"):
    print(f"Handling {file}...")
    with open(file, "rb") as in_handle:
        res = s.general.partition(
            request=operations.PartitionRequest(
                partition_parameters=shared.PartitionParameters(
                    files=shared.Files(
                        content=in_handle.read(),
                        file_name=file.name,
                    ),
                    strategy=shared.Strategy.AUTO,
                ),
            )
        )

        if res.elements is not None:
            # handle response
            pass

        with open(out_path / (file.name + ".json"), "w") as out_file:
            json.dump(res.elements, out_file, indent=4)
```

# Getting a Locally-Runnable LLM

This part is really easy, easier than it should be -- the [llamafile project](https://github.com/Mozilla-Ocho/llamafile) has executable files that already come with baked-in, pre-downloaded LLM models. In my case I'm going to get the example llamafile [hosted on huggingface](https://huggingface.co/Mozilla/llava-v1.5-7b-llamafile/tree/main).

I can `chmod +x llava-v1.5-7b-q4.llamafile && ./llava-v1.5-7b-q4.llamafile` and a browser will open, ready to teach me the mysteries of the universe.

# Finding the Right Stuff to Add to Prompts to Get The Thing

There are two general ways of finding text to inject into the prompts: Embeddings, which converts your text into vector space to represent it semantically and finding semantically similar items, and full text search, which does something easier to reason about and more traditional. Think a google search for a phrase.

## Doing Semantic Search

We're going to deal with _embeddings_, which is going from a pile of text into an n-dimensional list of numbers that somehow, mysteriously, represents that text's place in the world in the model. These embeddings vary from model to model and nobody knows what any of the numbers mean.

## Getting an embedding from text

Llamafile offers an easy way to extract an embedding from a string of text: the `--embedding` flag. So we can do `./llamafile --embedding -p "<Text goes here>"` and get back the embedding vector on standard out.

## Indexing our Transcripts with Embeddings

# Making it harder

[This blog post](https://techcommunity.microsoft.com/t5/microsoft-developer-community/doing-rag-vector-search-is-not-enough/ba-p/4161073) says we can't just do one. We have to do both. Maybe that's a task for another time.
