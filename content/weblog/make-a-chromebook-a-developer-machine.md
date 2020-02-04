+++
title =  "Turn a Chromebook into the ULTIMATE GOLANG/PYTHON DEVELOPER MACHINE"
date = 2016-12-26T01:11:45-08:00
tags = []
featured_image = ""
description = ""
+++

This is [a recycled post from my tumblr weblog](https://jason.cleanstick.net/post/155005051345/turn-a-chromebook-into-the-ultimate-golangpython) 

Ha ha ha just lying the real title should be

# Turning a Piece of Shit Chromebook into a Good Enough Development Machine Because You're Unemployed and Feel Like An Ass Trying to Justify Spending $2000 on a God Damned Macbook so You Wound Up Buying a Chromebook Instead

Anyway, I'm [unemployed because of reasons](http://www.theverge.com/2016/12/8/13887622/yik-yak-layoffs-growth-collapse) and figured there were better things to do with the credit limit on my credit card than spend $2000 on a Macbook, so I bought one of the highest rated Chromebooks at my "willing to pay this much" price point: [the Chromebook C100P](https://www.asus.com/us/Notebooks/ASUS_Chromebook_Flip_C100PA/). The stats are as follows:

* Processor: Piece of shit system-on-chip ARM thing
* RAM: Yes
* Screen: Acceptable but you can see the pixels
* Keyboard: Ugh

Considering it's still an order of magnitude better than [the first good laptop I owned](http://www.macworld.com/article/2901437/macbook/ode-to-the-12-inch-powerbook-g4-apples-first-desktop-quality-laptop.html), it's a pretty good buy at $200 and some change.

So Chrome OS is nice but I want to introduce security holes to the device, so *LET'S INSTALL PLAIN OLD LINUX*.

The first thing to do is follow the instructions to install [crouton via the instructions](https://github.com/dnschneid/crouton/blob/master/README.md). You get the option of what flavor of Linux to install, after 8 hours of experimenting with Debians and Ubuntus I found the one with the best support is Trusty. So do this after downloading crouton in Developer Mode:

    sudo sh crouton -r trusty -t xfce,touch,xiwi
    
"But I like Unity," you say. I respond with "NO YOU DON'T IMAGINARY IDIOT NO YOU DON'T NOBODY LIKES UNITY UNLESS THEY WORK FOR CANONICAL."

"But that is a very old Ubuntu," you say. Welp, the only big thing that will really matter is you'll have to load up an older `.tmux.conf` with the older mouse mode switches because that's all I found was missing. Everything else we will download from third parties.

Also follow the directions to install the Chrome extension in the host ChromeOS browser, it's helpful.

## Golang

Luckily the dudes at the Go project are charitable and offer an ARM version of the Golang toolchain. Go get a `-armv6l` version of Go [from the downloads page](https://golang.org/dl/) and decompress it in your home dir. If you use `~/workspace` as your Go home like I do, add this junk to your `.bashrc`:

    export GOROOT=~/go
    export GOPATH=~/workspace

Okay cool Go is ready to go. That last sentence's wording was not intentional nor was it a joke, get over yourself.

## Python

Trusty uses an older version of Python. Continuum's got it. [Get an `armv6l` installer of Miniconda](https://repo.continuum.io/miniconda/) and install it in your home dir. It'll even add itself to your `$PATH`. Python's covered.

## VS Code, the unlikeliest IDE

For some inexplicable reason [Visual Studio Code](http://code.visualstudio.com/) is the best IDE for writing Go. It's an indisputable fact and goes to further prove that we live in a cruel, arbitrary universe that often makes no sense. [This headmelted dude has you covered](https://code.headmelted.com/) for builds of VS Code for piece of shit ARM processors. Ignore his instructions, open a terminal in your xfce session and do this:

    wget https://code.headmelted.com/installers/apt.sh
    sudo sh ./apt.sh

now VS Code is installed. You can code in these two arbitrary languages I have chosen as my favorites on this awful hardware, and to be honest it's minimally painful (minus building huge Golang projects).