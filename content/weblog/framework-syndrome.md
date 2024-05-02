+++
title =  "Framework Syndrome: Solving Software Problems by Not Solving Them"
date = 2024-05-01T19:55:10-08:00
tags = ["work", "software"]
featured_image = ""
description = ""
+++

A common antipattern I've been both perpetrator of and victim to is what I describe as _Framework Syndrome_. This is the act of writing software that does not solve the inherent problem at hand, but provides a poorly designed scaffold in which one is expected to eventually "fill in the blanks." That is, in the absensee of the ability or desire to make the code do what it needs to do, kick the can down the road while at the same time writing mountains of not particularly useful code that will never be fully excised from th codebase.

# You Don't Understand the Problem, So You Code Around It

It was 2005. I was working on an early SaaS product for automating Intro to Statistical Methods courses for Psychology classes. We had a few functional requirements that I could do easily (user generation, logins, survey generators) and others I simply did not have the ability to do well (namely, actually do the statistical analysis that the grant required). So I worked around it. I added support to slice and dice data and export to Excel. I added natural language date parsing for forms. I polished the hell out of the admin interface. "This system is perfect," I declared, "we just need someone to plug in the code to do that one thing it was designed to do: statistical methods. You just need to drop it in...here. See how elegant it is?"

# "It Can Do Anything, You Just Have to Provide the Code"

Code that does not solve the problem, but provides an environment to add code that solves the problem, is ridiculous on its face. It's just another level of abstration that was added for the sake of engasging in the act of coding and not taking into mind any practical or business concerns.

# You've Done the "Fun" Part and Gotten The Credit, Someone Else Does the Actual Work

This is the unfair part of Framework Syndrome, and something that makes me deeply resentful when I run into it. A developer who arrives at the project first "designs" a solution, runs it past management, declares it Mission Complete, and moves on. The person who has to work within the constraints established by that long-gone person does the actual work that adds the business value, and is ignored by management.

# Let The Implementors do the Framework, Clean Up Later

From the resentment part of the section above, I propose that software be written in the following way:

1. Prototype written by domain expert as messy code
2. Professional engineers clean it up, finding common patterns across codebases and standardizing

By inverting the process from framework to solution to solution to framework, the frameworks themselves will be far more appropriate to the solutions they encompass.
