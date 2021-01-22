+++
title =  "Stupid simple API reference for bottle.py web services"
date = 2012-03-25T22:11:11-08:00
tags = ["bottle.py", "python"]
featured_image = ""
description = ""
+++

I have a stupid json-only REST API I implemented in bottle.py. This introspects the default app, gives a dumb readout that should act as an adequate reference for discovery:

```python
@bottle.route('/')
def index():
    bottle.response.content_type = 'text/plain'
    return ("=== API REFERENCE ===\n" +
            "\n".join(x['rule'] for x in
                      bottle.app().routes))
```
