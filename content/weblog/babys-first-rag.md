+++
title =  "A Practical Guide to Self-Hosting a RAG"
date = 2024-07-07T00:00:00-08:00
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
1. **Turnkey**: See the above point. I don't want this to be without speed bumps and be just a single command to get up and running locally. See the above point for my reasoning. If this could be "just for fun" I'd make it easier to do, but it has too much dangerous potential for evil.

## First Things First

We need a pyenv:

```shell
PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions" pyenv install 3.12.4
pyenv virtualenv 3.12.4 babys-first-rag
pyenv activate babys-first-rag
pip install -r requirements.txt
```

# Retrieval-Augmented Generation

## What The Hell is a RAG?

This was the hardest thing to get a simple answer for.

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

The [wget project](https://www.gnu.org/software/wget/) has been my constant companion since the early 2000s. `wget -r -l 2 http://somesite/` would quickly and reliably spider a web site two links deep onto disk. However, with modern sites (and abominations like [SPAs](https://developer.mozilla.org/en-US/docs/Glossary/SPA)) the HTML the client fetches is not the document tree that is ultimately established in the browser. So many pages are partially or fully rendered in Javscript now, requiring an entire bulky browser engine to derive the full DOM.

## Enter Playwright

[Selenium](https://www.selenium.dev/) came out many years ago for doing browser testing and I never really liked it -- it seemed unstable and finicky. A few generations later, we get a beautiful tool in the form of [Playwright](https://playwright.dev/), which gives us so much: Javascript and Python APIs, and simulation of multiple browsers, including the Chromium family and Firefox. It's really slick.

## Our Playwright Script

I'm going to start out by scoping out what I want to do:

1. Start at the first index page,
1. Find all the links to transcript pages on the index page,
1. Download the transcript pages,
1. Process the transcript data and place it in a database,
1. If there is a next button, click it and `GOTO 2`

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

I've got some boilerplate I can work with rather than starting from scratch, which is nice. Now I want to keep clicking _Next >_ until I run out of Next pages (and I checked, the next button is missing on the last page), so I modify part of the script as follows:

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

![DOM inspector screenshot](/images/babys-first-rag/dom-inspector.png)

With this we see that the links to transcript pages all have the class `hsp-card-episode`, so we can use Javascript to find them all on the page and pull out the link URLs:

```python
urls = await page.evaluate(
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

At this point I have the page's computed HTML, and I want to extract just the parts that are interesting. Let's put them into a JSON file I use for later manipulation and maybe insert into SQLite.

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

Unstructured is also my employer, so obviously they have an incredible team of attractive geniuses working for them and it's a good idea to buy as many commercial licenses as your employer can afford when you get back to work next.

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
                        file_name=file.name,
                        content=in_handle.read(),
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

### Getting an Embedding from Text

Llamafile offers an easy way to extract an embedding from a string of text: the `--embedding` flag. So we can do `./llamafile --embedding -p "<Text goes here>"` and get back the embedding vector on standard out.

We can write a python function that shells out to this program and returns an embedding vector:

```python
def embedding_for_text(text: str) -> list[float]:
    return [
        float(x)
        for x in subprocess.run(
            args=[f"{llama_executable} --embedding -p {shlex.quote(text)}"],
            stdout=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )
        .stdout.decode("ascii")
        .split(" ")
    ]
```

## Indexing our Transcripts with Embeddings

We're gonna want a table with each line item from the transcripts:

```sql
create table text_lines(
    filename text,
    text_line text
);
```

And then a virtual vec0 table:

```sql
create virtual table vec_chat using vec0(
    embedding float[2048]
);
```

### Inserting text into DB

Then we want to insert the text into the `text_lines` table:

```python
for file in folder.glob("*.json"):
    print(file)
    with connection as transaction, open(file, "r") as in_json:
        json_object = json.load(in_json)
        for item in json_object:
            if item["type"] == "NarrativeText":
                text = item["text"]
                transaction.execute(
                    "insert into text_lines(filename, text_line) values(?, ?)",
                    (str(file), text),
                )
```

### Premature Optimization: Use a Sliding Window

After a little bit of hacking, I decided to use an overlapping window of text items. Then, I noticed that longer bits of conversation could overwhelm the embedding processor later down the line. Here's what I wound up with as a heuristic sliding window generator:

```python
def _sliding_window(
    row_factory, window_size=4, overlap=1, min_length=20, max_length=80
):
    window = []
    for row in row_factory:
        if len(row) < min_length:
            continue
        elif len(row) > max_length:
            # Use long lines as implicit breaks
            if window:
                yield window
            yield [row]
            window = []
            continue
        elif len("".join(window)) > max_length:
            yield window
            window = []

        if len(window) >= window_size:
            yield window
            window = window[-overlap:]
        window.append(row)
    if window:
        yield window
```

Then I replace

```python
for item in json_object:
    if item["type"] == "NarrativeText":
```

with

```python
for text in _sliding_window(
    item["text"] for item in json_object if item["type"] == "NarrativeText"
):
```

### Adding Embeddings

Then we want to use `embedding_for_text` to add an embedding value to correspond with each:

```python
with connection as transaction:
    for row in transaction.execute("select rowid, text_line from text_lines"):
        rowid, text = row
        embedding = embedding_for_text(text)
        transaction.execute(
            "insert into vec_chat(rowid, embedding) values (?, ?)",
            (rowid, json.dumps(embedding)),
        )
```

### Kicking the Tires on Semantic Search

Let's try out a noat particularly controversial prompt (_Anthony Fauci, as head of the CDC, helped accelerate the COVID vaccine's release_) and see what the most semantically similar things our system is calibrated to inject:

```python
def nearest_n_neighbors(
    text: str, connection: sqlite3.Connection, limit: int = 5
) -> list[int]:
    limit = int(limit)
    with connection as transaction:
        return [
            x
            for x in transaction.execute(
                f"""
                    select rowid, distance
                    from vec_chat
                    where embedding match ?
                    order by distance
                    limit ?;
                """,
                (json.dumps(json.dumps(embedding_for_text(text))), limit),
            )
        ]


def nearest_n_text_lines(
    text: str, connection: sqlite3.Connection, limit: int = 5
) -> list[str]:
    with connection as transaction:
        return [
            row[0]
            for row in connection.execute(
                """
                    select text_line from text_lines where rowid in ?
                """,
                (
                    [
                        c[0]
                        for c in nearest_n_neighbors(
                            text, connection=connection, limit=limit
                        )
                    ],
                ),
            )
        ]

connection = llm_functions.fresh_db_connection()
print(
    nearest_n_text_lines(
        "Anthony Fauci helped release the COVID vaccine",
        connection
    )
)
```

That gives us:

```python

[
    "Right. Covid was a rerun of the AIDS chapter with AZT.\nBut the AIDS chapter seems even more terrifying because if the initial treatment was AZT, and we know AZT kills people, you're taking someone who has a compromised immune system and your response to that was give them something that's going to kill them quicker and then say there's a giant crisis and this is what Deusberg was demonized for.\nYeah, I agree. And for many years I resisted the interpretation. I was more familiar with Kerry Mullis's objections. Kerry Mullis was the inventor of PCR technology who died tragically, and some would say, strangely, at the very beginning of the COVID cris.\nHave you ever seen this piece of video where he talks about Anthony Fauci? Yeah, let's put it this way. Kerry Mullis was a outspoken, vigorous, highly intelligent person who was not corralled by fashion. And in fact, his objection to the idea that HIV was causing AIDS was an early testament to his maverick nature.",
    ...,
    "Chris Christie's a healthy guy and he wants to keep people healthy. He be covered. That should be the end of lockdown right there.\nHe did be covered so that whatever drugs they got.\nWell, I have a friend who is 80 and he just beat the shit, took some I.V. vitamins, said he was sick for four days.\nNew Jersey Governor Phil Murphy's highly confident marijuana will be legal. I look at him clapping.",
    ...,
    "So here's the thing. The controversial experiments and one lab suspected of starting the coronavirus pandemic and says the case against a human lab. And so it says why the human lab remains a suspect in the coronavirus investigation.\nI mean, it's really likely that we never really will know. But they most certainly were working on viruses similar to this one right there.\nAt the end of this article says there's another one called Rat RTG 13, which is very, very similar to the sars-cov-2 one that we're experiencing now. Oh, terrific.\nIt's thought to be the most similar to the sars-cov-2 of any known virus to share 96 percent of the genetic material, that four percent gap, but still be a formidable gap for animal passage research, says Ralph Burek, Virologist University, North Carolina, probably in bed with the Russians who collaborated with like when you found out that a Harvard guy got arrested, that because he was taking money from Russia or excuse me, taking money from China because he was doing something with them.",
]
```

All right, not terrible. It makes me want to punch my monitor which is a good sign.

# Trying it Out

## You Have to Post The entire Transcript Over and Over

One of the shortcomings of LLMs (with no escape that I know of) is the conversation has to _fully be injected into the LLM to maintain state_. So what I'll do is pipe an initial state with a question into the model, get the response from Llama, append a question, and do another round trip.

```python
def output_from_llama(text: str) -> str:
    return subprocess.run(
        args=[f"{shlex.quote(llama_executable)} -f -"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        shell=True,
        input=text.encode("utf-8"),
    ).stdout.decode("utf-8")[len(text) + 1 :]
```

From here we can cobble together a conversation.

## Not Very Good End Results

Well this was signficiantly dumber than I had feared:

```
Me:> What do you think about peer pressure?
Response:  As a language model, I do not have personal opinions or thoughts, but I can provide you with some information about peer pressure.

Peer pressure is the influence that peers have on an individual to adopt or act according to their values, attitudes, behaviors, and beliefs. It can be both positive and negative, as peers can encourage individuals to engage in healthy behaviors, such as exercising or studying, or discourage them from participating in risky behaviors, such as drug use or underage drinking.

In the context of the conversation, it seems that the participants are discussing aspartame, a sugar substitute used in many low-calorie and sugar-free products, such as diet soda, yogurt, and desserts. They appear to be debating whether or not it's poisonous, which could be an example of the influence of peers on each other's opinions about a certain topic.
```

In retrospect, the Joe Rogan transcripts are too information sparse and conversational to provide useful context for a conversation. But thinking peer pressure and aspartame are related is sure a silly one.

Here's a full log with the injected context of another short chat:

```
===== Final Log =====
Given the following information:
When it comes to podcast advice, maybe you should listen to the guy who might have invented it.
Four Americans from empowerment organization work with russian intelligence to spread propaganda.
What is the truth of that? Let's find out. Who is Klaus Schwab's father? At least his father did something.
Mike Perry, who's one of the bare knuckle fighters now. He's about as ferocious as a human being gets.
See, anybody that's in opposition to Putin has to be know it's the enemy of our enemy.
There it is right there. Subculture Vulture: A Memoir in 6 Seans by Mosha Kacher, available now. Did you do the audiobook?
You need weight classes. And then also, Joe also wants there to be no cage and have it on open.
Do I sound like an idiot if I say, who's Katherine Bach from the Dukes of Hazzard?
She's the goat. Greatest White House press secretary of all time. She's the best.
The tragic truth about Marilyn Monroe concealed intelligence. Thank you. During her fame, a lot of how Marilyn.
The wildest thing that most people don't know about the Nazis is how many we brought over here.

This is a conversation between User and Llama, a friendly chatbot. Llama is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision.

User: Who is the best prime minister?
Llama: It's hard to say who the best prime minister is, as opinions
User: What about the best press secretary?
Llama: The best press secretary is widely considered to be Katherine Bach, who served under President James Dukes of Hazzard. She was known for her wit, intelligence, and ability to handle tough questions from the media.
```

## Making it harder

[This blog post](https://techcommunity.microsoft.com/t5/microsoft-developer-community/doing-rag-vector-search-is-not-enough/ba-p/4161073) says we can't just do one. We have to do both. Maybe that's a task for another time.

# Conclusion

I put together the parts. I used a horrible source corpus. I learned a valuable lesson.

The important part is I was able to understand the pieces individually, I was able to host it on my own hardware, which I think is a very critical part of the LLM world nobody really thinks about since so much of it depends on cobbling together third-party services on the internet.

The code is all [on Github in an appropriately named repository](https://github.com/jasonbot/babys-first-rag).
