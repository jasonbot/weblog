+++
title =  "A (Mostly) Practical Guide to Self-Hosting a RAG"
date = 2024-07-01T00:00:00-08:00
tags = ["programming", "llm"]
featured_image = ""
description = ""
+++

{{< toc >}}

# Introduction

I promised myself (and, unfortunately, my manager) I'd implement a RAG from conception to finish by Valentine's Day, 2024. It is now Independence Day weekend. Missed the mark by a bit.

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

On the subject of the goal of _non-commercial viability_ and my love of making the world worse, not better, I present what I wish to do with a RAG here: take the transcripts of the Joe Rogan show and turn a chat bot into a poorly-informed, blubbering idiot.

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

# Finding the Right Stuff to Add to Prompts to Get The Thing

There are two general ways of finding text to inject into the prompts: Embeddings, which converts your text into vector space to represent it semantically and finding semantically similar items, and full text search, which does something easier to reason about and more traditional. Think a google search for a phrase.

## Making it harder

[This blog post](https://techcommunity.microsoft.com/t5/microsoft-developer-community/doing-rag-vector-search-is-not-enough/ba-p/4161073) says we can't jut do one. We have to do both. So let's do that, for maximum giggles.
