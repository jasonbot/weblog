+++
title =  "Pinebook Pro: The Tinkering Laptop"
date = 2021-01-19T12:11:45-08:00
tags = ["hardware", "pinebook", "vscode"]
featured_image = ""
description = "The Pinebook Pro is Neat"
+++

As the parent of an almost three year old, I don't get much time to myself, and I've given up on video games that don't have playtimes under 15 minutes (that discounts anything with load times or cutscenes). In my spare time I have to find other things to do that are low impact and can be cut into small amounts of time.

I've taken to watching a lot of retrocomputing stuff on YouTube, which has inspired me to tinker with old software and resource constrained devices. I've developed a newly renewed interest in hardware/software and gone fully into writing stuff like Lua and Rust on small ARM devices like RPis and [Pine64](https://www.pine64.org/devices/single-board-computers/pine-a64/)s.

I wrote before that I was going to buy a [Pinebook Pro](https://www.pine64.org/pinebook-pro/), and it arrived sometime last May. It came bundled with a flavor of Debian, but they started shipping with a blessed version of Manjaro in August or so. I wasn't happy with that decision because I am so familiar with the Debian ecosystem, but it was the official way to get proper GPU drivers for the hardware.

As common as the Arm64 architecture is in the world, it's mostly on mobile devices and not traditional "computing environments" like laptops and desktops. [Microsoft Visual Studio Code](https://code.visualstudio.com/updates/v1_46), for example, didn't have official Arm64 builds available until August of 2020.

First off is I've gotten back into game programming for my own amusement using [LÖVE](https://love2d.org/), which was just in Manjaro repos. I added Flatpak, Snap, and AUR support, but vanishingly few of those options have Arm64 builds, leaving me to revisit my times as a build/release engineer and build things from scratch.

Then, hey, why not Minecraft? These machines are still more powerful than the System76 laptop I owned over 10 years ago that I played the beta on. I found [a blog post](https://nicholasbering.ca/raspberry-pi/2020/10/18/minecraft-64bit-rpi4/) on getting it running (the two complications are getting lwjgl to build on the architecture and sidestep the fact that the latest versions of Minecraft use a native client to launch their platform-agnostic code). Building MultiMC following those directions worked fine, but Minecraft takes roughly 30 minutes to start and requires me to set the chunk render detch way down, so while it works in theory, it's unplayable in practice.

Then I thought I wanted to learn i3 to deal with the slowness of the Pinebook and make it more useful, and wound up choosing [Sway](https://swaywm.org/) and [Waybar](https://github.com/Alexays/Waybar). I almost got it usable but I had the option of 1) spending months redeveloping muscle memory or 2) customizing it so far into oblivion that I am the only human on earth who understands my idiomatic setup.

The usability of this environment was bad, and it mde me want something more traditional. I started getting weird and dark. I wanted to feel some nostalgia so I started building old desktop stuff. Like [AmiWM](https://www.lysator.liu.se/~marcus/amiwm.html) and [Windowmaker](https://www.windowmaker.org/) which led to me going ahead and build [the entire GNUStep stack](http://www.gnustep.org/) from scratch.

So I've been spending a lot of time on a highly resource contrained device building source from scratch and fighting with dotfiles. Years ago I would abhor this stage of getting stuff up and running, but nowadays it has an almost meditative, calming quality to it.
