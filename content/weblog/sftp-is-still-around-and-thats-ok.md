+++
title =  "SFTP is still around and that's OK"
date = 2021-02-18T08:00:00-08:00
tags = ["programming", "internet"]
featured_image = ""
description = "It's hard to get wrong"
+++

So it's 2021 and about the entirety of my job is integrating third party systems with internal ones, which then reach out to other third-party services.

A lot of stuff uses SFTP still. In this day and age anything not on HTTP seems barbaric, but SFTP does have its advantages.

# SFTP is format agnostic
This goes for HTTP as well, but you need to [correctly](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Encoding) [set](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) headers, and there's a constant, incessant push for change for change's sake.

# SFTP works for cold storage
SFTP servers are a known entity, and can be used to point at an old directory full of files somewhere, an enterprise-grade SAN, or whatever. It's file-focused where modern HTTP is more interaction/endpoint focused.

# The S in SFTP is already "secure"
HTTP is insecure by default, though in recent years yes, HTTPS is now almost a default (but not behind the edge, which is a story for another day).

SFTP starts via an SSH session with proper key negotiation. This means every workflow you do with SSH (like exchanging keys that are not necessarily signed by a root authority) is supported with SFTP. Having just written a downtime postmortem about a party not presenting a correctly configured certificate chain on their HTTP service, the fact that less can go wrong in SFTP is comforting.

# It's hard to get SFTP wrong
HTTP changes. To do something simple like send a file in chunks you have to set up an HTTP server correctly and support all kinds of [operating modes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) and implement [a bunch](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding) [of headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Length) and make sure both the server and client and any proxy handles it correctly. SFTP has significantly less cruft, significantly fewer implementations, and therefore significantly fewer configurations to thing about.

# SFTP semantically matches some workflows better
When you think about what you are doing, to download a batch file you:
1. Connect to a machine*
2. Go to the expected location
3. Download the file in a stream
4. Verify the file
5. Remove the remote file

\* Yes, this includes opening socket connection, doing TLS negotiation, and then authenticating, which are 3 additional steps to be berought into consideration

In HTTP, it's:
1. `HTTP GET` the location (steps 1, 2, 3)
2. Verify that locally (your application code)
3. `HTTP DELETE` the resource (provided the proxy/framework/application properly supports `DELETE`)

Since steps 1-3 are all enmeshed, you have to introspect on where the failure mode happened to figure out what went wrong. With SFTP it's

1. Connect to SFTP server (step 1)
2. `CD path` (step 2)
3. `GET file` (step 3)
4. Verify file locally (application code) (step 4)
5. `RM path` (step 5)

Semantically the steps to accomplish the workflow make it easier to wrap eachstep in a single try-except rather than have to dig into what went wrong in the HTTP transaction. The code, while simple, is simple. This makes it more readable and easier to both write and reason about.

# It's easy to consume
Consuming files via an SFTP client is as easy to do as consuming via an HTTP client, with signficiantly fewer failure modes.

# It works to keep the world working
[SFTP powers the financial world](https://www.treasurysoftware.com/ACH/ssh-sftp.aspx). Every day millions (billions? I honestly have no idea) of financial transactions are compelted via the ACH system, which is text files over SFTP. Similar batch jobs are completed for all kinds of similar systems which may be mainframes running COBOL or "cutting-edge" Enterprise Java rats' nests of code copying files over to a Linux machine somewhere to expose them to the world.
