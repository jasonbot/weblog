+++
title =  "Classicube at Work"
date = 2024-11-20T08:00:00-08:00
tags = ["programming", "work", "go", "minecraft", "games"]
featured_image = ""
description = "How I wired together a thing"
+++

# Problem Space

At [my new job](https://www.academia.edu/), my new team engages in a team activity: every other week we get together for 30 minutes to play a game together online. We're mixed hybrid, meaning about half of us work in office and half of us are grandfathered/exceptioned in to working remotely. this means we can't play a board/card game in person, but has to be procurable over the internet in a Zoom call.

It is now my turn to host a game.

# Picking a Game

I'm sure everyone is tired of playing Werewolf and variants at this point. I wanted something easy to pick up in the spirit of the games we've played on game days since I joined:

- Casual
- Multiplayer
- Browser-based
- Very low barrier to entry

I don't want to pick Yet Another Card Game. That sounds boring.

# Minecraft?

[One retro YouTuber I like](https://www.youtube.com/@ActionRetro) pretty consistently plays [ClassiCube](https://www.classicube.net/) on the hardware devices he features in his videos. This seemed like a pretty good option: lower software requirements then MC Java Edition, as well as not requiring a paid account to play. It even [has a browser-based client](https://www.classicube.net/server/play/) that can connect to servers.

[ClassiCube has documentation on Github for how to run a browser-based session](https://github.com/ClassiCube/ClassiCube/blob/master/doc/hosting-flask.md).

This seems pretty easy: you host a web page that has the ClassiCube JS client on it, and then configure it via Javascript in the page's code to connect to your hosted server.

## Of Course I Have To Write Software to Run Software, It is My Wont

The end product I made was [Cube With Friends on Github](https://github.com/jasonbot/cube-with-friends). It's a very easy to set up little program that does all the above manual steps -- at build time it embeds all the resources it needs from the internet into a single Go executable, and has other niceness like overlaying a pre-authored config that turns off ClassiCube authentication so people can join without having ClassiCube accounts.

# Getting to It From Other computers

Now that I had something running, how do I get other players on here?

I spun up `cube-with-friends` on my laptop and started thinking my way through that problem.

## Hosting on the Internet

I don't want to sacrifice one of my Raspberry Pis to be a permanent host for this app, and I'm not going to mess with seeing if I can get to the public IP that my ISP assigns me.

I don't want to spin up a new VM on GCP and assign it a Real Internet IP Address and do all the work of exposing a service to the world if I can help it either.

## Hosting on Tailnet

Here comes an idea: my employer pays for a Tailscale corporate account, and all of our dev machines belong to the work tailnet. This is good, I can just point everyone to my work Mac.

### I Don't Want to Put a Personal Device on the Work Tailnet

My Raspberry Pi Collection has begun to dwindle, and I am not a fan of putting personal devices on work networks anyway.

### My Work Mac Has a Firewall I Can't Disable

As is corporate policy, all of our work laptops have a firewall we can't turn off. I can run Cube with Friends locally but the TCP ports are blocked.

### I Don't Want to ask the Infra Team How to Host a Minecraft Server, That's Embarrassing

I could host a machine on the Tailnet on our corporate Infrastructure, but I'm not on the infra team and I don't know how to do that. I also don't think I'd get buy-in for that. I'll save my goodwill for some other day.

## Running a Non-Firewalled Machine: How About Linux?

### Rub Some Docker on It

I quickly threw together a preliminary Dockerfile to make an image of a cube-with-friends instance, and started making progress. Now how to get it on the Tailnet?

[This guide to using docker-compose to make a container join a Tailnet](https://tailscale.com/kb/1453/quick-guide-docker) made me very sad at the complexity involved, but hopeful. I could run a Docker container on Linux, have the container join the Tailnet, and it would not be subject to the macOS firewall on the hardware network interfaces.

I switched from Docker Desktop to [Colima](https://github.com/abiosoft/colima) a few years back -- I've been moving away from using brand named Docker utils for a while now since 1) Docker has a [weird licensing tripwire](https://www.docker.com/pricing/) I don't want to set off and 2) [containers are just a commodity](https://github.com/containers/) in 2024 -- I use Podman on all my Linux machines to do containerization.

Colima just works, and [has multiple personalities](https://github.com/abiosoft/colima?tab=readme-ov-file#runtimes) which was useful at my last job for dicking about with k8s and stuff.

### CoLima is Short for "Containers on Lima"

[The Lima Project](https://github.com/lima-vm/lima) implements the underlying functionality of running a Linux VM on macOS that can then host the containers, since containers require [Linux kernel internals](https://lwn.net/Articles/236038/) to work ([or not](https://wiki.freebsd.org/Containers)).

Why not short-circuit the process and just use the VM directly? Why bother with another abstraction layer? I'll just use Lima directly and not make myself sad with the extra abstraction layer that a `compose`-based solution im-...poses.

## Starting a New VM

So I:

- Cloned the repo `git clone git@github.com:jasonbot/cube-with-friends.git`
- Started a new VM using `lima create default`
- I edited the configuration so that my auto-mounted home drive was `writable: true` before launching (this is important if you're keeping the cloned repo on your Mac home dir and not on the VM)
- Installed prereqs: `sudo apt install golang mono-runtime`
- Ran `lima` to get into the VM
- Edited the `/etc/hostname` to something memorable
- Restarted the VM
- Went back in via `lima` and Installed Tailscale via `curl -fsSL https://tailscale.com/install.sh | sh`
- Signed in to tailscale `sudo tailscale up`
- Ran the cube-with-friends server: `go run cmd/server.go`
- Opened a browser to `http://my-new-machine:5555/` and verified it worked

# Conclusion

So there we go! Something a little more interesting than playing another card game.

![Login Screen](/images/playing-classicube-at-work/ss1.png)

![Success -- logged in](/images/playing-classicube-at-work/ss2.png)
