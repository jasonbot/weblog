+++
title = "I Don't Like that I Like Starship"
date = 2025-10-29T00:00:00-08:00
tags = ["software", "programming"]
featured_image = ""
description = "Custom $PS1s: threat or menace?"
+++

> I have [my seed Starship config](https://gist.github.com/jasonbot/26e894be371417ee20b973c0def1d366) up as a Gist.

[Starship](https://starship.rs/) is a tool that frustrates me because it seems so bikesheddy and unneeded: a custom prompt manager. We already had shell prompt customization! I blindly install `oh-my-*` on new machines for prompt customization! And it's in Rust. People just use Rust to be cute.

Then I realize that it's okay to have nice things. The command line environment from the 90s can change. `rg` doesn't suck. The `lazy*` TUIs don't suck. I mock [Textual](https://textual.textualize.io/) and [Charm](https://charm.land/) openly and unrepentantly and still hypocritically use and enjoy the tools built with them. The terminal is changing because the people using it have the agency and hubris to use it differently.

I can have a growth mindset and accept that

1. The preferred command line tool to do a thing can change in my lifetime and
1. The preferred workflow to accomplish a task can change in the face of new tools and
1. The people who invented the old tools we're replacing were not gods, they were just as fallible as us so
1. Writing new tools that learn hard lessons from decades of using the old ones is fine. It's not sacrilege.

But its killer features:

- **On rails/opinionated**: Other prompt customization schemes I've used have let you do _anything_, but you had to know _how to do anything_. I can't think of cleverness I want in my prompt, I just want to see which Git branch I'm on. We're all doing that. We all want that. [Starship has a way to do that](https://starship.rs/config/#git-branch) which isn't brittle bash I have to maintain myself.
- **Multiplatform**: I have Windows Bash, Windows PowerShell, Linux Bash/Zsh, and macOS Bash/Zsh all driven by the same seed config. I can have it show the same information everywhere. I can use little emblems to let me know if I'm on my Mac, on a Linux machine, if I'm on Windows and if that's PowerShell or Bash all right there.
- **The Nerd Font Dark Horse**: This system takes advantage of [the glyphs](https://www.nerdfonts.com/cheat-sheet) in [Nerd Fonts](https://www.nerdfonts.com/) and normalizes abusing them. This adds the additional "burden" of installing a Nerd Font enabled typeface on all my apps with terminal editors, but I've already normalized that.

So here it is. All this talk for something that doesn't _look_ substantively different but compounds into _feeling_ different over the course of the days and weeks I use it:

![Image](/images/starship/starship.png)
