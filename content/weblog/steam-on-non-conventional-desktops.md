+++
title = "Steam on non-Conventional Desktops (Niri)"
date = 2026-01-17T00:00:00-08:00
tags = ["games", "linux"]
featured_image = ""
draft = false
+++

I'm trying out [Niri](https://yalter.github.io/niri/)! You know how I [encourage getting used to the defaults](/engineering-virtues/the-defaults/)? Well [I'm not following my own advice](https://github.com/jasonbot/dotfiles/tree/master/linux/_config/niri)! I'm using it with [Dank Shell](https://github.com/jasonbot/dotfiles/tree/master/linux/_config/DankMaterialShell) too, [also ignoring my own advice](https://github.com/jasonbot/dotfiles/tree/master/linux/_config/DankMaterialShell)!

Anyhow! One liner! If Steam isn't working do this: edit `/usr/share/applications/steam.desktop` and change the `Exec=` line to this:

```ini
Exec=bash -c "wl-copy --clear && /usr/bin/steam -system-composer %U"
```
