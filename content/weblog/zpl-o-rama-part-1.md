+++
title =  "ZPL-O-Rama Part 1: A personal/work project (Introduction)"
date = 2021-03-08T00:00:00-00:00
tags = ["software", "hardware", "web", "programming", "zpl-o-rama"]
featured_image = ""
+++

# Introduction

In my spare time on weekends in between errands and mornings before everyone wakes up, I've been working on a little project I've been having a lot of fun with: ZPL-O-Rama.

# The Problem

A large part of my employer's line of business is creating shipping labels, and a large number of those aren't simply printed images, but printed on very high volume, heavy duty, industrial grade printers using [a proprietary language called ZPL](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf).

In an aggressive and justified act of Intellectual Property enforcement, there are no legal software ZPL renderers available<sup>1</sup>. This means that to test the output of a ZPL stanza we have to physically print a label and inspect it. In the Before Times of 2019, our office was full of all kinds of ZPL printer we could freely and cavalierly print to.

Now that workplaces are in a [post-office diaspora](/weblog/thepost-office-world), we no longer have access to ZPL printers. The fleet of printers were  dispatched to a number of people in the org who opted in and had a vested need to test ZPL. I was one of those people.

Now, for those without a printer, if they need to test something they will go into a Slack channel and hope someone sees it in a timely manner, prints teh ZPL, takes a picture, and reports back.

We can do better than that. We can automate this.

_Footnotes_

**1.** (Yes, I am aware of [Labelary](http://labelary.com/viewer.html), but that's also proprietary and probably in violation of all kinds of agreements)
