+++
title =  "A Children's Treasury of Critiques and Concerns about the Current LLM Hype Cycle"
date = 2025-03-03T00:00:00-00:00
tags = ["llm"]
featured_image = ""
description = ""
+++

We're a couple of years into the LLM hype cycle and the volume at this point is _deafening_. I use LLMs, and I find them interesting, and they have played a major part of my professional life for the past three years.

That said, I can't declare them an unqualified success or a miracle cure for anything. I approach them with a combination of skepticism and grief. I understand they are here to stay and I will do my best to use them effectively in the use cases where they are indeed effective. However, I think it is both foolish and irresponsible to myself, my employers, and society in general to seem them solely in a positive light and think we need to think critically about how we want to approach them.

# How LLMs are Made

As an undergraduate and a couple of years into my post-university life, I did research in what could be considered "natural language processing" or "computational linguistics": I worked on the [HAL Model](https://link.springer.com/article/10.3758/BF03204766), which was an early high-dimensional model for approximating language understanding, and later [a software system employing all kinds of cool cutting-edge techniques](https://dlib.org/dlib/january03/mitchell/01mitchell.html) (early Support Vector Machine tooling being one I worked on) and there was one lesson I learned from both:

> **Better models are good, but better data is _better_.**

Far and away, the best way to get better results was not to develop a better model, it was to develop toolchains for collecting more and better data. We got good results even with okay models when we fed them Wikipedia. We got bad results even with cutting edge models if we just fed them a couple of emails. Good data was what made these things effective.

That said, it paints my experience of the current success of LLMs: they are interesting technology from a modeling perspective, but the more interesting part is _all the data that went into making them_.

## LLMs Are Not Sourced from Above-Board Places

Even "open-source" models do not share their training sets. We have no idea where these impressive troves of training data have come from. We know that there are pirated books in Meta's Llama models for sure. Screenwriters' Guild protected screenplays have shows up in other datasets by virtue of the fact that there are pirated copies on the internet, which the training sets then integrate. Nobody's getting paid money if their work is added to an LLM. The value is contributed by armies of human authors, and the profits, whenever they may come, are collected by the companies using the data.

Spotify's model is genius in that it barely pays its artists. OpenAI's model is even better: it doesn't pay its artists at all. It doesn't even acknowledge that humans _made_ the fuel it needs to go.

You can argue that people consented to use their 'content,' which is a sterile way of simplifying any product a human being can express into words, be it art, opinion, fact, conversation, etc., but _not everybody consented_, there is non-consensually acquired material in them **right now**, and many people, knowing now what their data is being used for, _want ways to possibly opt out of consenting in the future_. A Reddit user is screwed, essentially, in that a community they have spent decades of sweat and tears contributing to is now just training data to a robot somewhere. They're going to have to _sever their relationship with their friends and community on Reddit_ in order to stop feeding a machine they do not like (or are fundamentally, ethically opposed to), which did not exist 7 years ago.

## LLMs Are Not Up-to-Date

All models rely on their training sets, which are fixed at a point in time. To get accurate information beyond the date a model was trained, you need to do one of three things:

- Create a new model with the additional up-to-date information (expensive)
- Fine-tune an existing model with additional up-to-date information (expensive, error-prone)
- Inject contextual data into your prompt sessions with things like extended context windows and RAG architectures (these work all right in practical use, I would say this is the least bad traded for now)

Even a model that is trained last week will not be able to tell you the current weather.

# How LLMs work

## LLMs are Non-Deterministic

LLMs are not predictable, and I mean this in two ways:

1. Given an input, there is no reliable way of getting the same output every time
1. This is exacerbated by models being a 'black box' -- OpenAI or Anthropic can make tweaks to the model, putting out a slightly different training on the model, change temperature parameters, even by _hosting the same system on a new data center_ you can get wildly varying, unpredictable results.

If we can't depend on an LLM to reliably do the same thing the same way every time, it's not nearly as dependable as a simple machine in a factory.

I would not want my car randomly changing its gear ratios every time I left it in a parking lot.

## We're Already Approaching their Upper Limits

We've seen emergent issues with LLMs that give us pause and act as comical, widely-published issues that these things aren't armed with the unlimited potential they claim to have:

- Prompt injection
- The Strawberry problem

In every case, we're finding limits to the technology that get fixed in the next release, but are something of an indicator that we are no longer in the world of boundless possibilities and uninterruptible optimism for what they are capable of: the problems get fixed in subsequent models with what are essentially "bugfixes" to work around these cases. **We aren't discovering substantially new, greenfield capabilities with new LLM models anymore, we are in a stable "bug fix" phase**.

I'm copying a graph from an old book ([_Putt's Law_](https://en.wikipedia.org/wiki/Putt%27s_Law_and_the_Successful_Technocrat)) to demonstrate my thoughts here: we're rounding the _success_ intersection point, everyone is projecting a straight line up, we're going to slow down at some point.

![S-Curve Law](/images/llms/s-curve.svg)

### Band-Aid 1: Tools and the MCP

One way that we're getting around the recency and context problem is with _tool-call enabled models_.

Just as a human being can use a pocket calculator, we can give an LLM access to a calculator tool to do math, which LLMs structurally can't do like humans can.

Just as a human being can use a web browser to look up weather, we can give an LLM access to a weather API (or, more roundabout, a browser automation that can open a weather web site).

Just as a human being can use a search engine to find relevant information, we can give an LLM a tool to search through masses of text and use that to enhance its answers.

### Band-Aid 2: Injected Context (RAG)

Very similar to the last point above with the search engine, we can make an LLM "know" things not baked into its model by pre-emptively doing a search engine queries on its behalf and by injecting snippets into its conversation context it can "know about" in its context to appear to be able to comment on user-relevant data.

Some models now have larger context models in which the RAG approach is 'obsolete,' but technically the methodology is the same: inject massive amounts of non-model data into the context to get the LLM to 'know' about it.

# How LLMs are Monetized (Theft and Planned Enshittification)

LLMs as a business plan don't seem very viable long-term unless they engage in some major enshittification. Enjoy ChatGPT and Claude at affordable rates without embedded advertisements now, because as soon as they're a part of your workflow they're going to bet _real bad, real fast_.

1. They are an incredibly expensive product to make (millions of dollars to train one)
2. Sold for well below the price point needed to recoup the cost of their production (OpenAI and Anthropic are running comically massive losses)
3. Replaced with newer models at a dizzying pace, with no real way of comparing them apples-to-apples (see the disjoint and inconsistent "benchmarks," which themselves are gamed by vendors and can't be trusted)
4. While themselves becoming commodity products within days of their release (each model immediately is replaced with a new one)

# LLMs In Usage Are Just A Reminder Of What We Once Had

LLMs are, in essence, a lossily-compressed, fuzzy searchable copy of the internet (and a lot of pirated material).

Google used to be good. We used to be able to type these things into Google and get answers. Using an LLM as a search engine is just an indictment that through slow decay of Google's core product functions and the fact that we can't have nice things -- SEO monsters started posting garbage on the internet to game the search engines and ruined it for all of us.

Your chat with an AI session is a sad, watered-down echo of a quality user experience we once had a quarter of a century ago with a single text input box on Google.com.

# Widespread Adoption in LLM is in its Uber/AirBNB Phase

I like to tell people that commercial LLMs are in their Uber phase, and I mean this in two ways: 1) they are blatantly illegal and hoping to normalize their bad behavior through mass adoption and 2) priced in a way to hook you, to get you dependent on using it in fiscally unsustainable ways.

## Normalizing Lawlessness

When Uber and AirBNB were first entering widespread release, there was immediate backlash: these things were illegal. Uber famously paid its drivers' fines and tickets for operating as drivers, and AirBNB lobbied the hell out of local municipalities. Both

We're all engaging in intellectual property theft right now when we use these models. They're betting on a "they can't arrest all of us" approach in which the norms and laws which worked are forcefully changed to further enable this theft of creators' property.

Again: the value of the LLMs is the data, not the model, and human beings have to provide that data. Large LLM companies are only going to be profitable if they are allowed to use data at very small margins, if not zero cost (stealing training data with impunity).

I have not heard a single compelling case for the unequivocal legality of what's going on: every assertion I've seen that OpenAI has a 'right' to this data is qualified with an _apparently_ or a _probably_.

## The First Taste is Free

I remember when every Uber ride was heavily subsidized by its investors. I could Uber Pool to multiple venues across San Francisco for about $10 on an evening out. Now that Uber has to be profitable, I don't even consider it except as a strategic last choice, and it's significantly more expensive now (that same night out now would run me $75).

Don't fool yourselves into thinking that once your default choice is 'I'll ask ChatGPT' that ChatGPT won't find a way to squeeze for as much as it can because it's insinuated itself into your lifestyle.

# LLM Tools as Developer Aids

This is something that I see regularly on my radar as a software engineer. _I USE LLM CODE ASSISTANCE_, but _I do not think it is worth the trouble at least 75% of the time_.

## An LLM Assistant Is Trained On Already Written Code

Languages and frameworks that exist today can be handled no problem, but if we limit ourselves to what models are trained on, we can't adopt new languages, frameworks, libraries. An LLM-guided software engineering world is a world where software engineering is frozen in time.

## Writing Code Is Probably The Easiest Part Of Coding

Writing code is usually an exploratory process for me in which I 'feel out' the problem space. I very seldom use plain English to describe my problems because English is less precise and less able to express to the computer what I want it to do. It's also harder to write. We use programming languages because they're good at telling computers what to do. Telling a computer to write its own code by asking it in English is just adding a step.

Not to mention that fact that _reading code is always harder than writing it_. We have let the computer do the easy part and asked it to inflict the hard part on us from minute one of the code existing. By letting the tool do the coding _we're adding cognitive load to a process that already worked fine as-is for many of us_.

## Maintenance is Job None

LLM-generated code can only be up to about two years old at this point (early March 2025). In my 2+ decades of software engineering, getting a product out _is_ important, but then there are years, if not decades, of follow-up fixes and expansion on that software. We have no idea how maintainable LLM-assisted codebases will be, and there are already examples of LLM-driven code growing beyond the scope of e.g. Claude's ability to understand them and leaving the developers high and dry; unable to understand or extend the existing code.

I've fixed Fortran that was older than myself at one point. Getting a new React app out is not the hard part, it's the toil of maintenance that happens over the course of years that is where most of what I would consider "software engineering" happens and it does not seem like that has been a focus or a strong point of LLM-driven development thus far.

## Every Prior Advancement in Developer Productivity Followed a Pattern Entirely Unlike this One

I don't think an LLM is going to steal my job. Every change in technology that made developers more productive over the last 50 years has only increased the demand for software, and every productivity boost that was supposed to cut the number of people needed to make and run software has only grown the number of people involved. Examples: your startup probably has more Infra/DevOps engineers than a startup of the equivalent size had Sysadmins in the pre-cloud era. CRUD apps becoming easy to make with better tools led to a Cambrian Explosion of people writing CRUD apps.

Usually improvements to the craft of software engineering have been via _better tools and languages_. In the instance of the LLM-assisted coding world, we have given up on the idea of inventing a better programming language and have instead decided we can't do any better and are using non-deterministic macro expansion/copy-paste agents in the form of LLM-enabled development tools.

This would be like C never taking off because someone invented a better assembly macro processor, or Python/Ruby/etc never taking off because the interpreters could never get memory management right. We'll just ask an LLM to translate our machine code into a different machine code, rather than find an appropriate way of expressing these computing concepts in a better way.

# How LLMs are Sold

I'll say this is my least objective or reasonable prong critiquing LLMs as they are currently practiced, but the strongest one I go to when asked what I think about LLMs: **cheerleaders are fucking annoying**. When I hear ridiculously stupid, not-backed-up-by-evidence claims about what LLMs can and will do I immediately knee-jerk block the person for being so stupid. The people who know the least about what they are talking about are being the loudest.

We _had_ "agentic" software before, it was just called "computer programs" or sometimes "automations" or "APIs" or "integrations" or "cronjobs." The generic term "AI" was hijacked to represent LLMs and only LLMs, and the terms for traditional software were unnecessarily thrown away for a new term for the same thing. _There is so much marketing baked into the terminology_. We've gone from arguing the virtues of the thing to arguing based on pure enthusiasm for the thing.

# Conclusion

I pose the following questions (the answer to some of these are unequivocally _yes_, but they are still important to keep in mind):

- Are LLMs, in general, an improvement to what was there before?
- Are LLMs, in your specific cases, worth the financial cost? Will the be worth it at 2x the cost? 10x?
- Are the benefits of LLMs worth the _social_ cost?
  - Are you willing and able to live in a world in which creative work is impacted in a transformatively negative way?
  - Are you able to look to your friends and peers and tell them that anything they produce in written form belongs contribute to the public good without compensation?
- Do LLMs make coding _better_, or just _different_?
  - Are you actually more productive using an LLM agent to code, or it it just novel?
  - Are you aware of what you are giving up in terms of control and understanding when yielding control to an LLM?
  - Are you willing to give up that understanding and control long-term?
  - Are you willing to take personal responsibility for code you did not personally write?
  - Are you willing to take the risk that generated code derived from models trained on GPL-licensed code may taint your codebase?

You may come to the conclusion that yes, LLMs are worth it. That's fine. I just hope you went though a process of thought and introspection and considered the pros and cons of the technology before loudly and enthusiastically adopting them into your life.
