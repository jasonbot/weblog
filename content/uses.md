+++
title =  "Tools I Use to Live My Glamorous Life"
date = 2024-12-14T00:00:00-00:00
tags = ["uses"]
featured_image = ""
description = "Another /uses page, just like the others"
+++

# Development

## Languages/Technologies

- I am primarily a Python expert (25 years!)
- I am primarily a [FastAPI](https://github.com/fastapi/fastapi) user, and I am better than average at doing async programming (which sucks and is bad, but it's fun to do bad things)
- I primarily choose Postgres as my database
- I do most of my personal dev projects in Go
- Over the last 3-5 years, Typescript has become the dominant language I use at work
- If you ask me to write something in C++ I will say no but I _will_ write C++ to spite you
- I prefer Linux on the desktop to Mac on the desktop at this point
  - I do not value my time or sanity
  - If something is reliable, I get bored and self-destructive so I need to be in a state of crisis in all aspects of my life and a Linux desktop fills that need in this space
- I now prefer Fedora and Fedoralikes for desktop Linux
- I usually prefer Debian stable or one of its relatives for servers and Alpine for container base images
- I use [Tailwind](https://tailwindcss.com/) at home for CSS, often [tableflipping and reverting to vanilla CSS](/weblog/tailwind/)
- I use [Solid](https://www.solidjs.com/) and [plain old JS](https://developer.mozilla.org/en-US/docs/Web/JavaScript) at home, [React](https://react.dev/) at work
- I use [Ollama](https://ollama.com/) on Windows, Mac and Linux to locally run LLMs

## Editors/Environments

- My muscle memory is [Vim](https://www.vim.org/), I use it everywhere
- I have hit the point of no return and use [Zed](https://zed.dev/) more than anoy other development tool
  - I no longer use LLM code assistance in any measurable amount, I find a lot more value using LLMs as code review tools than code generation tools
- Much of my polyglot development is via [VS Code](https://code.visualstudio.com/)
- I like using [Ebitengine](https://ebitengine.org/) to make silly 2D games
- I also (rarely) play around with [Picotron](https://www.lexaloffle.com/picotron.php), [Pico-8](https://www.lexaloffle.com/pico-8.php), [TIC-80](https://tic80.com/) and [LÖVE](https://love2d.org/) for the same

## Command line

- [Here is the bootstrap set of dotfiles I use](https://github.com/jasonbot/dotfiles) on new computers
- On Windows, [I'm doing the same thing but different](https://github.com/jasonbot/bootstrap-windows-development-machine) with setting up a new machine.
- I use zsh and bash almost equally, though I think I have more zsh machines now
- I usually start out with [oh-my-zsh](https://ohmyz.sh/) or [oh-my-bash](https://github.com/ohmybash/oh-my-bash) on new systems
- I use [nvm](https://github.com/nvm-sh/nvm), [rbenv](https://github.com/rbenv/rbenv), and [pyenv](https://github.com/pyenv/pyenv) to manage node/ruby/python installs -- I can't get the hang of [uv](https://github.com/astral-sh/uv) but that looks like the future at this point for Python.
- I use `grep`, [`rg`](https://github.com/BurntSushi/ripgrep) and [`ag`](https://github.com/ggreer/the_silver_searcher) in descending order of frequency
- I like [git-delta](https://github.com/dandavison/delta) for command line diffing
- I like [lazygit](https://github.com/jesseduffield/lazygit) for some easy to explain but harder to do than necessary git operations. Sometimes a GUI (or a TUI) is nice! Not everything has to be commands or code!
- [lazydocker](https://github.com/jesseduffield/lazydocker) loads a hell of a lot faster than any other offering for looking at running containers in a reasonably high level way

### It Came from Userspace

- I always add `~/.local/bin` and `~/bin/` to my `$PATH` so I can manage my own binaries without superuser perms
- I download [VS Code](https://code.visualstudio.com/download) and [Go](https://go.dev/doc/install) (setting `$GOPATH` to `~/.go`) from tarballs and manage them myself, adding `~/go/bin` and `~/VSCode-linux-x64/bin` to `$PATH` -- that way I don't need to deal with native packages or elevated install permissions
- Same with [Deno](https://deno.com/)
- Currently in `~/bin`: `btm` `slirp4netns`[^1] `tmux` `tic80` (static binaries acquired from their release pages)
  [^1]: This is missing in ChimeraOS for some reason and the only part absent from a working podman setup on my handheld

## Cloud Stuff

- In the past, I did [Terraform](https://www.terraform.io/)
- A couple of jobs ago, I learned a little [Pulumi](https://www.pulumi.com/)
- At most places of employment, I use [AWS](https://health.aws.amazon.com/health/status)
- I had to learn [Azure](https://azure.status.microsoft/en-us/status) at my last job
- At home, I use [GCP](https://status.cloud.google.com/) for personal projects

# This Site

- The theme for this weblog is a no-longer-recognizable fork of [smol](https://github.com/colorchestra/smol), built in [Hugo](https://gohugo.io/)
- Hosted on [Github Pages](https://pages.github.com/) through the magic of [a CNAME](https://docs.github.com/en/github/working-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site).
- **Fonts**: I'm using [Forevs](https://ohnotype.co/fonts/forevs), [Instrument Sans](https://github.com/Instrument/instrument-sans) and [0xProto](https://github.com/0xType/0xProto) (hosted here with this page and not on Google Fonts).

# Productivity

## Producing and Manipulating Visual Artifacts

- [Xara Photo and Graphic Designer](https://www.xara.com/us/photo-graphic-designer/) as I have muscle memory and it's fast to make drawings in
- [The Gimp](https://www.gimp.org/) for quick raster touchups
- [Inkscape](https://flathub.org/apps/org.inkscape.Inkscape) to touch up SVGs
- [Mermaid](https://mermaid.js.org/) for diagrams extensively because it's everywhere, mark a code block as `mermaid` in markdown and you get the rendering for free in things like Obsidian and on Github
- [Monodraw](https://monodraw.helftone.com/) for cool text-mode diagrams
- [D2](https://d2lang.com/) for diagrams as code -- I like it in terms of how clean the language looks, how clean the output looks, and how easy it is to use
- [Graphviz](https://graphviz.org/) comes along for the party, too -- it's old but it gets the job done for a large range of jobs

## Desktop Apps

### Windows

- I have [a script I wrote for work](https://github.com/jasonbot/bootstrap-windows-development-machine) to boostrap a new Windows machine; it installs and configures most of the tools below
- I run [Win11Debloat](https://github.com/Raphire/Win11Debloat) immediately upon starting on a new Windows desktop machine
- [Winget](https://github.com/microsoft/winget-cli) is a command line utility built into the operating system you are sleeping on.
- [Windows Terminal](https://github.com/microsoft/terminal) for my terminal emulator
- [Powertoys](https://learn.microsoft.com/en-us/windows/powertoys/) for various tweaks, [the runner in particular](https://learn.microsoft.com/en-us/windows/powertoys/run) is nice
- [Notion Desktop](https://www.notion.com/desktop) to do work
- [Notion Calendar](https://www.notion.com/product/calendar) as my calendar
- [SyncThing](https://syncthing.net/) to move files around

### Mac

- [BetterDisplay](https://github.com/waydabber/BetterDisplay) for better external monitor support
- [SyncThing](https://syncthing.net/) to move files around
- [Notion Calendar](https://www.notion.com/product/calendar) to see what I'm supposed to be doing
- [Notion Desktop](https://www.notion.com/desktop) to do work
- [Rectangle](https://rectangleapp.com/) to move windows around
- [Enchanted](https://github.com/AugustDev/enchanted) as a standalone frontend to Ollama
- [Ghostty](https://ghostty.org/) as my terminal emulator

### Linux

- [Syncthing](https://flathub.org/apps/me.kozec.syncthingtk) to move files around easily
- [Rhythmbox](https://flathub.org/apps/org.gnome.Rhythmbox3) to handle my large music library
- [Boxes](https://flathub.org/apps/org.gnome.Boxes) for light virtualization work
- [Podman Desktop](https://podman-desktop.io/) for container-fu
- [virt-manager](https://virt-manager.org/) for my Windows VMs
- [Prism Launcher](https://prismlauncher.org/) to play Minecraft with my kid
- [Alpaca](https://flathub.org/apps/com.jeffser.Alpaca) as a standalone frontend to Ollama
- [Steam](https://store.steampowered.com/about/) for Steam
- [Ghostty](https://ghostty.org/) as my terminal emulator

## Networked Software

- [Mastodon](https://github.com/mastodon) for one Fediverse server
- [GotoSocial](https://gotosocial.org/) for the other
- [Miniflux](https://miniflux.app/) for keeping up on news
- [Forgejo](https://forgejo.org/) for hosting my private repos

# Computer Hardware

## General-Purpose Computing and Development

I have a handful of computers I use regularly!

- An older Legion desktop running [Nobara](https://nobaraproject.org/) for gaming and general computing
- [Pinebook Pro](https://pine64.org/devices/pinebook_pro/) running [Manjaro](https://manjaro.org/products/download/arm) for remote terminal stuff and as a lightweight Miniflux client
- [AOKZOE A1](https://aokzoestore.com/products/aokzoe-8-inch-amd%C2%AE-ryzen%C2%AE-6800u) running [ChimeraOS](https://chimeraos.org/) for handheld PC gaming, also using its Gnome desktop as a portable development setup
- [Whatever the smallest iPhone is](https://en.wikipedia.org/wiki/IPhone_13) on the market at the time for doomscrolling

## Toys

- [Shanling M0s](https://en.shanling.com/article-IntroM0s.html) for listening to music outside of my home office
- [RG35XX](https://anbernic.com/products/rg35xx) running [MyMinUI](https://github.com/Turro75/MyMinUI) for video games during my commute hours
- [Flipper](https://flipperzero.one/) that I never break the law with

# Non-Computer Hardware

- The [Peak Design Everyday Backpack](https://www.peakdesign.com/products/everyday-backpack) as a backpack
