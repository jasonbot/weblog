+++
title =  "Oh, Goddammit: I'm back on C++ in 2026"
date = 2026-10-02T00:00:00-00:00
tags = ["c++", "programming", "work"]
featured_image = ""
description = ""
+++

The title for my autobiography would probably be _I Thought I Was a Child Prodigy But I Was a Late Bloomer_. Going from being the youngest guy in the room to the oldest guy in the room happens suddenly, violently, and permanently. As such, the programming languages and technologies

# Why C++

Quite simply: Windows APIs. Obscure ones. They come with C++ headers and opaque `.lib` files and COM interfaces that fall well outside of the coverage footprint of [`windows-rs`](https://github.com/microsoft/windows-rs). I'm writing [RDP plugins](https://learn.microsoft.com/en-us/windows/win32/termserv/dvc-server-apis), which with some gymnastics I could do in Rust but it would be a lot more work to do the cooler thing. And I'm doing [Citrix channels](https://developer-docs.citrix.com/en-us/citrix-workspace-app-for-windows/citrix-virtual-channel-sdk-for-citrix-workspace-app-for-windows/introduction.html), which are straight up C++ or Go Fuck Yourself (I believe the SDK docs explicitly use this language).

But there are old features that aren't exposed to moderns tacks that give us easy wins that exist on users' systems without additional upgrades or installs. The RDP client bridge binary I wrote is under 50k. It builds in 3 seconds. It runs on every Windows machine. Hot fuck on balls, that beats the 50 minute Typescript BDSM sessions I engage with on CI at work.

Here are some good things about C++:

- You can easily link in legacy C and C++ code
- There is a lot of legacy C and C++ code you can integrate quickly and well. I chose [miniaudio](https://github.com/mackron/miniaudio) as a lowest common denominator for audio processing (and miniaudio is not 'legacy', it is a modern project on a conservative stack) and it took 2 hours to get a working Linux build out of my Windows code.
- It's easy to write node.js bridges in it: I even use Objective-C++ for my macOS integrations
- "Modern" C++ has a lot of features that make it less awful to use -- I'm pinned on C++20 and `std::variant` and `std::visit` gives me structural pattern matching. `nlohmann::json` is one of the cleanest JSON libraries I have used in any languuage and it's _just a header_
- Compile times are blink-of-an-eye fast
- Build stacks are _just there_ on every system
- It's fun to spite people who uncritically adopt shiny things like Rust

# Why Not C++

LLMs I guess
