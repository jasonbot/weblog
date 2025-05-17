+++
title =  "Search"
tags = []
featured_image = ""
description = "Search the Site"
+++

{{< raw >}}
<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<script src="/pagefind/pagefind-ui.js"></script>
<div id="search"></div>
<script>
    window.addEventListener('DOMContentLoaded', (event) => {
        new PagefindUI({ element: "#search", showSubResults: true });
    });
</script>
{{< /raw >}}
----
Powered by <a href="https://pagefind.app/">Pagefind</a>.