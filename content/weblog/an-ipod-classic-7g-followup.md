+++
title =  "A Revival of Sorts: Where I Wound up With my iPod Classic 7th Gen"
date = 2026-10-01T08:00:00-00:00
tags = ["hardware", "music", "apple"]
featured_image = ""
description = "It's an MP3 player with a liver of copper"
+++

I've been using my iPod classic as my sole music player all summer now. The
replaced screen, battery, storage, and front shell are all steady.

I've found myself on an alternate build of Rockbox called
[Rockpod](https://github.com/nuxcodes/rockpod); the main thing I like about it
is very superficial: it changes the theme colors based on the playing track's
album art. It also claims other features that probably matter like being
flash-aware so it treats flash storage like flash and not like spinning metal.

However, the firmware also chokes on MP3s that are not 44kbps. So I have to
re-encode everything that isn't that bitrate.

So now I have a system that works:

- Reboot the iPod in stock firmware for disk use (it randomly trips of its feet
  and stops working when you copy lots of files)
- Treat the music library not as a _synced copy_ of my core music library but a
  _transformed copy_ -- the Rhythmbox library is the point of truth and the iPod
  data is an adaptation of it that plays on the iPod.

I'm not a huge fan of LLMs, but they can reduce toil in some cases. OpenCode was
running a free trial of [Ox Alpha](https://oxalpha.com/) one long weekend so I
used the free tokens to help me shape my itch-scratch tool:
[`rockbox-db-refresh`](https://github.com/jasonbot/rockbox-db-refresh).

I use the script to see what files are missing from the iPod, re-encodes them as
needed, and checks Musicbrainz for missing album art.

It can also update the stock firmware's itunesdb, which was a nice to have when
the tokens were free but I don't use much.

In all, this piece of 2005 technology still _feels good to use in 2026_ because
_everything in 2026 sucks so badly_.
