+++
title =  "A Revival of Sorts: Getting my iPod Classic 7th Gen Working Again"
date = 2026-07-02T08:00:00-00:00
tags = ["hardware", "music", "apple"]
featured_image = ""
description = "It's an MP3 player with a heart of gold"
aliases = ["/weblog/an-ipod-6g-revival/"]
+++

I've been very happy with my [Y1 MP3 player](/weblog/innioasis-y1/) over the
past 9 or so months. I take it with me everywhere! It's a companion on my
commute, it's a focus tool in my open office, it's a way to have a
single-purpose device that doesn't have the distractions of my glass Everything
Rectangle and, as the phone ages, a way to mitigate its now-horrible battery
life by using a different device with a different battery. As God confounded the
language and scattered the people building the tower of Babel, I have confounded
the functionality and scattered the responsibilities of the apps on my iPhone.

My wife brought up a point that is completely fair: why am I using this
$60 piece of crap when she, through great sacrifice, bought me a top-of-the-line
iPod Classic 160GB for the same purpose? Sure, that was in 2012, but it was
_expensive_. It's still worth $350+
today, right?

So what the hell, I dug it out of my Closet of Cables and Mystery. Plugged it
in. Battery charged. It booted. My music was still in it, last addition to the
library was 2014. Fantastic! I bought a protective case, some new 30-pin USB
cables because the ones I had remaining were all frayed and kind of scary, and I
got ready to swap the Y1 with the iPod for a while as an experiment.

Then my first hurdle: I wanted to add some songs to it. I know
[Rhythmbox](http://www.rhythmbox.org/), my player of choice[^1], has an iPod
plugin on its list of installed plugins. I plug the iPod in, it shows up!
Hooray!

I try to drag music onto it: no dice. Checking `dmesg` I see some very
threatening notices that HFS+ with journaling is not supported by Linux _at
all_. So I know on Mac it's a simple command line call to turn journaling off on
a volume so it's probably a trivial process, but I have no working personal
Apple desktop machines. Have no fear:
[I found a chunk of unvetted C that directly alters the raw filesystem](https://gist.github.com/noderat/c8929d41342bc6b63954)
to do it for me on Linux! Boom! We're in business!

Back to Rhythmbox. Drag the music I want over to the iPod. It copies! Bingo!

Only: no bingo! I disconnect the iPod and it says 'no music.' The music is on
the device, but the iPod's music database got clobbered. Well crap.

So now I know [Gtkpod](https://github.com/trinitonesounds/gtkpod) is purpose
built for this. Apparently the iPod Rhythmbox plugin isn't any good on these
models, so let's try that. No dice. It repeatedly hangs, crashes, and when it
does work it still fails to correctly update the database. Still 'no music.'

Maybe this is all because it's still HFS+ and not FAT? It seems like most tools
assume you've liberated your iPod and you're using it in Windows mode, not Mac
mode. So I attempt to wipe the drive, but can't for the life of me figure out
how to do it _correctly_ with Gtkpod or just plain old partitioning tools. Looks
like I need to restore the hardware from iTunes for this route.

What about [Rockbox](https://rockbox.org/)? I use it on my Y1. The annoying
thing is that I have to manually update the database on the actual device,
whereas the typical iTunes stock experience is one that updates the database
iteratively as a matter of course of adding music. But the trade-off is no more
struggling with Gtkpod and friends, which is higher friction than the
drag-and-drop experience of putting music on my Y1 anyway. And
[I saw this totally cool skin on Reddit I want to try](https://themes.rockbox.org/index.php?themeid=4073&target=ipod6g)!

I already have the Rockbox utility on my machine from installing it onto my Y1.
It sees my iPod but dies on an SSL handshake talking to rockbox.org while
downloading resources. I don't remember this happening last time I ran this. I
downloaded and ran the utility on another Linux machine and got the same result.
I gave up about 45 minutes into building the tool myself from source.

Damn.

Now I need a Windows machine to use iTunes in Windows to reformat the iPod. I
have a debloated Win11 VM in Gnome Boxes, I fire that up and go in to iTunes, I
plug in the iPod, then I go to set up USB forwarding so the VM can do its magic
and -- "USB Forwarding is Not Supported in the Flatpak version of Boxes."

So I uninstall the Flatpak and migrate my disk images from
`~/.var/app/org.Gnome.Boxes` to somewhere less Flatpak-specific and install the
dnf version of Gnome Boxes. I migrate the machine over, set up forwarding,
everything seems to be working.

Only USB forwarding forgets the device when it disconnects and I have to
reconnect multiple times. It also doesn't see the device when it's in that raw
flash mode, so it can't forward to install the iPod firmware. This is a dead
end.

Okay, so I have one Windows machine in my house: my kid's 2013 Intel Macbook
with Boot Camp and a debloated copy of Win10 we solely use to play Minecraft
Java together with. Only ever since I set up a local server with GeyserMC and
Floodgate we've been playing mixed me-on-Java/him-on-iPad-or-Switch-Bedrock so
the laptop is mostly neglected.

So I install iTunes and wipe the iPod. Takes awhile, because I have to install a
cascading series of drivers, but it eventually works. The firmware was the
latest for the Classic, released 2009.

Then I remember that 18 year old bit of early enshittification of iTunes: the
iPod can't simply be its own library you add/remove items from.
[I was falling out of love with Apple about that long ago](/weblog/osx-less-and-less/),
and I had forgotten how low and slow we've been dealing with the world of You
Will Own Nothing enshittification that's been inflicted on us. No wonder we're
so complicit, we're pushing a quarter century of Everything Rental now. So to do
iTunes proper I'd need enough storage on this laptop to hold the music in my
library on it, be logged in, and sync a selection of it to the iPod. I remember
this now: they made life harder and worse on purpose. And now we have Spotify,
where we never had freedom or affordances at all. I remember thinking what an
incredible act of charity it was that Spotify let your have an offline playlist
on your device. I would have expected offline first as _a matter of course_ in
prior hardware/software cycles.

Rhythmbox and Gtkpod still don't sync correctly. Same database issues, so
nothing I'd done with wiping the iPod had fixed the fundamental first issue.

Rockbox.

So I install the Rockbox utility on the Windows machine. I have to install some
additional Windows components to get it to load, but it works. I flash the iPod.

It doesn't boot.

I flash it again.

It boots. Hell yes. And I have my cool theme.

So I drag music over. 16000 tracks to start, takes 2 hours to copy. HDDs are
_slow_[^2]. Afterward I have to manually update my database from Rockbox, which
takes _hours_. I fall asleep as it runs. I can hear the physical spinning
platters. It's a very strange experience having a device with a real life
magnetic disc hard drive again. The future we occupy today is strange in the UX
of the iPod and its software feels modern enough but small aspects like an HDD
feel anachronistic.

The Rockbox experience is a lot nicer on the hardware it was designed for than
the crappy Rockbox-in-emulation on an Android device that has absolutely no
business whatsoever claiming it can run Android. It is responsive, it doesn't
crash, all the plugins work, etc.

Next rabbit hole is investigating battery/storage upgrades. There are cheap and
expensive options, I need to go through them. As is my wont, I do not need
Bluetooth on anything I own, but a modern USB-C connector might be nice? Do I
want to go the SD card route or a proper SSD?

That is for another time.

Anyway, no normal person would inflict this experience on themselves willingly,
and would likely give up at some point close to the beginning. It is a reminder:
much like if you stay very quiet near a playing iPod you can hear the whirr and
rattle of the HDD, and if you stand very quietly near me you can hear the
fluttering and tapping of dozens of moths smashing their bodies against the
inside of my skull in the space where a brain should be.

[^1]:
    I am not aware of any other MP3 player that can handle large music libraries
    this well and still have a presentable UI. TUIs usually suck, "new" apps are
    all super slow because of Wirth's Law.

[^2]:
    Though not as slow as I initially thought: transferring files in and out of
    the device is hampered by USB 2.0 speeds, but the seek times of the HDD are
    bad. There were two bottlenecks in the file transfer stage, HDD seeks/reads
    are also slow but faster than the Universal Serial Bus.
