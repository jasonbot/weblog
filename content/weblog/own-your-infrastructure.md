+++
title =  "Own your infrastructure"
date = 2020-02-04T16:45:45-08:00
tags = []
featured_image = ""
description = ""
+++

I've been sharecropping on Amazon's server farms since I moved to the Bay Area 5 years ago. That is, every startup I've worked for has utilized AWS (and sometimes GCP or Azure in addition).

This started out great for my career because I have not built a server machine from parts out since I was in college and I could use all my developer muscles to be operations person.

However, when you're on-call, you no longer own your uptime. Amazon will randomly flip bits. Its hosted services will go down without warning and leave you helpless but to wait -- you're down until Amazon Hosted Whatever Thing decides to go back up (and the status page will lie about it being up).

Now I'm at a new place where the systems team (I am back in plain old Software Engineering, hopefully out of DevOps forever) actually runs data centers. Everything is done in VMs and not containers. And it's so refreshing. Not only can we be 100% responsible for fixing downtime, but it provides a much stabler and less abstract system to build software on top of. When the solution to a problem is "this Bash script" and not "this Byzantine pipeline only one guy understands" it makes the infrastructure easier to reason aboue and less prone to failure.