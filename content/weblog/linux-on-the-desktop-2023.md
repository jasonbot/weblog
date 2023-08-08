+++
title = "2023: Linux on the Desktop This Year"
date = 2023-08-07T01:11:45-08:00
tags = ["linux", "hardware", "programming"]
featured_image = ""
description = "We keep doing this"
+++

I have a Gaming PC I bought from Costco when my wife told me "I should maybe get back into my old hobbies" in the summer of 2020. It came with Win10, which is fine and it's probably good to have at least one Windows machine in the house at any given time.

The thing is: Windows is _annoying_. Every time Windows ran an update I had to run [a third-party uninstall tool](https://www.wagnardsoft.com/display-driver-uninstaller-DDU-) to undo the changes Windows updates made to the graphics drivers, which started hanging and crashing if they weren't the exact specific ones the machine shipped with.

We had a flood in the winter of 2022. Our new home office was under half an inch of water and many of my electronics were unsalvageably water damaged. I placed this gaming machine (which hardly got any usage anyway) outside to dry.

The case then accrued condensation inside, which cvonvinved me this thing was now, if it had not been previously, fully water damaged e-waste.

In April I was bored and wanted to see if I could at least save the hard drives before taking the machine to recycling. On a lark I tried to turn in on and surprise surprise, it booted no problem!

Since I had already written it off as "dead," I figured it was fine to put Linux on it. I had read about [Nobara Linux](https://nobaraproject.org/) as it was done by the same guy who does a bunch of Proton and SteamOS hacking, and it had a bunch of quality of life improvements to make it gaming friendly: it even had the Steam client installed out of the box. Once I got over my distaste of using a non-.deb based distro I was off to the races.

I like the Gnome desktop. This ships with a newer version of it.

For the whole "I need at least one Windows machine in the house" thing: Proton plays all my games. Steam on here does 95% of what I need. TYhe only Windows app I _really_ need is [Xara](https://www.xara.com/photo-graphic-plus/), because I've been using it or its lineage since 1999 and I have muscle memory. Every attempt I've made in every flavor of Wine has failed, and even [the Linux versions they briefly released](http://www.xaraxtreme.org/) are now too bit-rotted to be usable on a modern installation on an x64 machine.

So Wine mostly has me covered, but for that single app I'm now using [virt-manager](https://virt-manager.org/) to handle a single [Tiny10](https://archive.org/details/tiny-10-NTDEV) install, which is a custom "remix" of Windows that is so bare bones that it's not even possible to install the [new Windows terminal](https://github.com/microsoft/terminal) on. But it's got a very small footprint and it runs my programs and is _probably_ a better idea than an XP VM.

So Nobara has been fine for the past several months. I have [VS Code as an RPM source](https://code.visualstudio.com/docs/setup/linux#_rhel-fedora-and-centos-based-distributions), I just download Go as `.tar.gz` and plop it into `~`, Python via `https://github.com/pyenv/pyenv`, google cloud command line apps, and [Flatpak](https://flathub.org/en) has turned out to be this amazing dark horse over the past 3 years to find decent software in a distro-independent fashion, the only annoyance remaining is that there's the occasional double-buffering-flicker thing that pops up on 3d accelerated UI apps.
