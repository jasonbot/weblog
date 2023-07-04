+++
title =  "VS Code: Dark Terminal on a Light Theme"
date = 2023-05-28T08:00:00-08:00
tags = ["programming", "vscode"]
featured_image = ""
description = "I like different color schemes"
+++

I'm a weirdo: on my IDEs I prefer a light theme, having used light themed IDEs since time immemorial (still miss using Visual Studio regularly). But I prefer white on black for my terminal emulators, as I have used that since time immemorial and a black on white terminal window doesn't feel like a serious thing.

So here's what I added to my `settings.json` to get the best of both worlds (light theme turned on):

```json
  "workbench.colorCustomizations": {
    "terminal.foreground": "#ffffff",
    "terminal.background": "#303030"
  }
```

Simple enough!

**Update:** [This site](https://glitchbone.github.io/vscode-base16-term/) has a panoply of copy-pastable terminal themes.
