+++
title =  "ZPL-O-Rama Part 4: The Hardware"
date = 2021-03-08T04:00:00-00:00
tags = ["software", "hardware", "web", "programming", "zpl-o-rama"]
featured_image = ""
+++

# Hardware

## The RPi

The Raspberry Pi is a (I think) Pi 3 with Wifi I found in the garage with a cheap clear acrylic case. It might have been a RetroPie rig in a prior life? Or one I was "gonna get around to" doing something with and finally did?

Then for this project I bought a Raspberry Pi camera and a small acrylic case for it, too.

## The Printer

The printer is a hefty boi, a Zebra something or other. It belongs to work. It has an ethernet port, a lot of lights, an air of proprietary grandeur, and a hunger for paper and electricity.

## THE ASSEMBLED RIG

I wanted all the components to be as easy to transport as possible, so I used adhesive velcro tape to affix the components to each other and some adhesive cable maangement clips to hold the cables in place, carefult to leave enough slack so that the side dfoor can still open.

The Pi is running stock Raspian, I have the Pi connected to the printer via a short span of Cat 6 I found, and I'm using dnsmasq's dhcp bound to `eth0` so that the printer always gets the same IP that the Pi can address it through. The Pi joins my network via WiFi. The intent is for the whole mess to be easy to pick up and move around the house.

The last piece is a humble power strip.


A picture of the front (you can see some of the cable management):
![Hardware Rig Picture](/images/zpl-o-rama/rig-picture.png)

How it's set up:
![Hardware Rig Diagram](/images/zpl-o-rama/rig-diagram.svg)

[On to part 5 →](/weblog/zpl-o-rama-part-5)
