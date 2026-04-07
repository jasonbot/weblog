+++
title = "Golang Webview Installer for Wails 3"
date = 2026-04-04T00:00:00-08:00
tags = ["golang", "programming"]
featured_image = ""
description = "Here I Go (this is a pun and I regret it immediately)"
gomodvanityhost = "jasonscheirer.com"
gomodvanityrepo = "https://codeberg.org/jasonbot/webview-installer"
aliases = ["/webview-installer", "/weblog/webview-installer/"]
+++

> **Top Matter**: [Codeberg for the library](https://codeberg.org/jasonbot/webview-installer), [doc for the library](https://pkg.go.dev/jasonscheirer.com/webview-installer).

I've forked [Lea Anthony's library](https://github.com/leaanthony/webview2runtime) that eventually [made its way into core Wails](https://github.com/wailsapp/wails/tree/b748b4625724b36f406d17987335805a83751093/v2/internal/webview2runtime) for two reasons:

1. I want it in Wails 3 and it's not there
2. I want to shave a meg off the binary size by not providing the embedded installer exe

So here we are.
