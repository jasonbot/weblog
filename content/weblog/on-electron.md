+++
title =  "If Your Electron App is \"Just A Browser Wrapper\" You're Doing It Wrong"
date = 2025-12-06T00:00:00-00:00
tags = ["work", "programming", "web", "c++"]
featured_image = ""
description = ""
+++

Having spent the last 6 months working on [an Electron app full-time](https://www.notion.com/desktop), my Stockholm Syndrome has kicked in and I've come around to it.

It's easy to disparagingly refer to an Electron app as bloated, or a crappy wrapper around a web app. This is lazy, reductive thinking that travels well in short-form media like TikTok and Elon Musk's _𝕏: The Everything App_.

> I'm going to say this in so many words over an over in here: do you hate Electron out of
>
> 1. Groupthink,
> 2. Out of misguided and impractical engineering aesthetics, or
> 3. Because you would prefer the "bad" apps you see written in it to not exist at all, over existing but being kind of bad?

That is, is the framework that allows bad apps to proliferate _bad on its own_ for enabling bad programmers or _good_ for enabling _skilled and unskilled programmers alike_ to participate in software engineering? Or _both_?

Oh my oh my do I love being ambivalent on everything and I want to pass that along to you.

# Electron Isn't Just A Browser Wrapper

Aside from wrapping a web page, though, is [a whole truckload of stuff](https://www.electronjs.org/docs/latest/api/app) to make a carefully and comprehensively written Electron app _actually good_:

- Window creation and management
- Menus, you know, like system menus
- Custom tray icons
- Dock icon overlays
- Apple Touchbar customizations (RIP)
- Opting to run the app on startup
- Sending crash reports to interested parties
- Writing additional native code in native languages like C++ and Rust via Node extensions _that give better platform-specific runtime characteristics_.
  - I can use the native filesystem.
  - I can use native builds of machine learning libraries with hoping you're patient enough to watch them run slower and worse in Webassembly.
  - All of a sudden things that ran slow on your computer or non-privately on some SaaS company's server are happening _quickly, efficiently, on your hardware on your desk_ with _no network round-trips_.

And more! And after all this, it happens to let you place rectangles in those windows that are views into the Chromium rendering engine.

If an Electron app you're using doesn't _feel_ mostly native, it's more an indictment of the nature of the people making the app than the framework they're using.

The whole point of Electron is to provide a decent, native desktop experience and uses HTML/CSS/Javascript as its core language for user interface and the Nodejs runtime and its ecosystem behind the curtain. Familiar tools, fast development. Development that is only _feasible_ in many cases.

# If You're Distributing Containerized Apps or Static Binaries You're Just As Guilty of the Original Sin of Electron

We already have `libc` back at home. An Electron installation doesn't use system libraries. This is a conscious choice. An Electron app comes batteries included. You can afford 250 megs of HD space for an app you use daily, you disk cheapskate.

Electron bundles all that inside itself. It's the equivalent to a static binary that doesn't use the system libc. It's the equivalent to a full-blown, dozen-gigabyte Ubuntu system with apt-get and superfluous apps installed as an image base just to host a single node app in a container. You accept batteries included software elsewhere: don't be a hypocrite and complain in this case.

## The Operating System Webview is a Lie and a Nightmare and Probably Worse than Nothing

The words in the subheading immediately above about cover it. I was using another webview-based framework (who cares which) for [an app](https://codeberg.org/jasonbot/ollama-desktop-with-wails) and I had a pretty cool UX with sidebar tabs that rendered vertically to save space via [text orientation](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-orientation). The webviews in 50% of the platforms I tested didn't do this, they rendered the text horizontally, breaking my UI. Flexbox wasn't fully there. Some of the platforms (Linux) didn't even support changing fonts _at all_.

I now had another variable I had close to zero control over regarding my rendering engine. I now had web technologies, inconsistently applied, that I had to _extensively_ test on every platform. I could not trust my UI to be a UI.

Packaging a rendering engine gives me guarantees of rendering capabilities independent of the operating system's webview. I can't tell a paying customer "sorry man that's just the way it is on Windows 10" with a straight face.

# It's a Way Safer Bet to Just Use HTML for UI

## Longevity

HTML and Javascript have a long, unbroken 30+ year lineage in which improvements have been additive: never destructive (except maybe the demise of `<marquee/>`), and never a full fork (except that now-extinct misadventure into XHTML).

The W3C is run by the most bureaucratic, glacially-paced working groups sponsored by the most hatefully pedantic employees at the largest, most inertia-driven tech companies in the world. This means that toy features that are unlikely to have a long lifespan won't get into the working spec. A bunch of orgs all have to agree to implement the feature in their parallel implementations before the feature's really considered usable. None of us is as obstructive as all of us.

The only extant UI frameworks I am aware of with the same relative longevity are X11 and Win32, and neither of them have been capable of the degree and pace of modernization that HTML/CSS/JS have had. (I will include QT in a respectable but distant third place here after Win32 and X).

I can tell you that picking whatever "rapid" XAML horror Microsoft is currently pushing is a bad idea! You're going to need specialists who are hard to find to work on it when it is discontinued for the Next XAML Horror.

## Portability

This goes without saying: Chromium runs on every major platform. Most browser engines outside of Chromium are also multiplatform (Firefox, Servo, Ladybird). The part that draws the pixels on the screen draws the pixels the same everywhere. It covers the whole "exposing OS native components in a cross platform way," up to and including accessibility mechanisms built on OS-level buttons and text. It's a good way of describing user experience in code that works pretty well on every modern device.

## This is the Only Realistic Way you Clowns are Getting Anything Nice on Linux

As a volunteer open source enthusiast, I can see myself pouring hours of love and care into a Linux-only app that faithfully and elegantly follows the Gnome HIG. I cannot see myself doing this for a paycheck. I am willing to endure that pain for the sake of my art, but not for the sake of closing out issues for customers.

Easy ports from Win/Mac to Linux are the most likely way you're going to see your app on Linux, and Electron is probability-wise the most likely way to get there. I can't justify putting more than 1% of my work hours on builds that only reach 1% of our user base. I just can't do that at work. If I can get 75% overlap for Linux by parasitizing my Windows and Mac dev time via Electron, you're more likely to get a Linux app. If it's just another build target with a very small amount, hopefully 1% total, on platform specific issues, you have a chance of seeing it on Linux.

## Hiring

Large organizations are risk averse. This means they want interchangeable resources to avoid bottlenecks. Humans are resources, just ask your Human Resources department. Being able to pull from the largest possible pool of frontend engineers with no training required is a feature, not a bug.

It's also an inconsiderate move to trap your engineers in dead-end technologies. If a replaceable frontend engineer has 5 years of fully non-transferable experience on your proprietary frontend, when _you_ throw them away due to _your_ idiot budget decisions _they_ have to write off 5 years of their lives on their resumes. That framework isn't applicable elsewhere. Boo on you, you monsters. Using an industry standard, "safe" framework is "safe" for employee and organization both.

# Conclusion

Electron is a low risk way for large organizations to add desktop features to something that originated on the web (probably a Node/React boilerplate app that grew past its original purposes, let's not lie). You need to ask yourself the question when you see a bad Electron app: is this better than nothing? Did Electron simply allow the app developers to unleash a usability nightmare on you? Or did it enable them to provide a nice, uniform, _native-enough feeling_ application that might be bulky and aesthetically unpleasing from a software engineering perspective but is in practice a workable experience?
