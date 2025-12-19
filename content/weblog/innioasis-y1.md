+++
title =  "The Innioasis Y1 Music Player"
date = 2025-11-15T08:00:00-00:00
tags = ["hardware", "music"]
featured_image = ""
description = "It's an MP3 player"
+++

# Introduction

I've been enjoying standalone MP3 players lately! The [Innioasis Y1](https://www.innioasis.com/products/y1) kept coming across my radar, I like the form factor, it was $50.

What the heck, why not.

# And Then

The community for this thing is _insane_, it's just as active as the people doing weird things with [my RG35XX](/weblog/rg35xx/). It's really cool seeing so many people doing neat things with such a simple piece of hardware. And like the RG35XX, part of the value proposition is this is a cheap peice of commodity hardware that would not have been possible in this way even 5 years ago, but is now inexpensive enough and flexible enough to be an incredible product for the money.

# Rockbox

I saw you could put [a flavor of Rockbox on the thing](https://github.com/rockbox-y1/rockbox) so I did that. The UI out of the box isn't nearly as polished but [there's a neat community-supported updater](https://github.com/y1-community/Innioasis-Updater) that goes so far as to install skins for you. I'm currently using [another Adwaita adaptation I found on the y1 subreddit](https://codeberg.org/joelchrono/AdwaitaPod-Arcticons-rockbox-360p) which handles CJK correctly, which turns out to be important to me.

Rockbox has the ability to create a play log file, so [I can scrobble my commute/work listening again](https://www.last.fm/user/jasonbot)!

I use the [LastFMLog plugin](https://www.rockbox.org/wiki/LastFMLog) to manually create a `.scrobbler.log` file, then use [rb-scrobbler](https://github.com/jeselnik/rb-scrobbler) to upload it. It's a manual process I only do every week or so, but it's okay.

This is awesome.

# Final Thoughts

Three surprises. Not quite complaint territory but worth knowing about:

- No external storage. My Shanlings had a TF card slot so I could expand and swap the storage easily. This is internal. 128GB so it won't hold my whole library but it holds everything I care about.
- No touchscreen. Again, coming from Shanling this took a little bit of getting used to. Pure iPod classic ergonomics, buttons only.
- Build quality is not super solid. The screen is plastic, not glass, and it scratched almost immediately. You can definitely "feel" a center of gravity while the majority of the device fgeels light. No metal in its construction. It doesn't feel brittle but by no means is it a luxury experience.

This thing is a lot of fun to use, though! The novelty will eventually wear off but it feels good to have something iPod shaped in my life again.
