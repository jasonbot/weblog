+++
title =  "There and Back Again: My Journey Into (And Out Of) Tailwind"
date = 2025-07-23T00:00:00-00:00
tags = ["css", "html", "programming"]
featured_image = ""
description = "I Like Tailwind, I went through stages"
+++

I've been using [the Tailwind CSS Framework](https://tailwindcss.com/) for abut two and a half years (as of July 2025) for my personal projects, and I used it professionally in my time at [unstructured](https://unstructured.io/) as well. In all, I think it's a good thing. However, I don't find myself thinking I'd use it for new projects at this point: I believe I have outgrown it. Here is a short story.

# Tailwind as Style Guide

Tailwind has a set of that encourages a [specific styling worldview](https://en.wikipedia.org/wiki/Linguistic_relativity) that gets you a "modern" looking UI which doesn't feel offensive versus any other site on the internet. The [pre-baked color choices](https://tailwindcss.com/docs/colors) and reasonable framing around [layout options like columns](https://tailwindcss.com/docs/columns) give you a framework (ha!) within which to work and make a decent site. It's less greenfield than a blank page and an [open documentation tab](https://developer.mozilla.org/en-US/docs/Web/CSS).

# Tailwind as Tutorial

I've been doing web development on and off for...well, since my teenage days but I don't specialize in frontend dev and every few years when I come back to focus on it, things have changed. I don't know what's popular, I don't know what's possible, I don't know what's popular (hint: if it's easy to do in CSS, it's popular).

[Flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox) in particular is something I had a somewhat superstitious, vague understanding of. I could do little bits and pieces and sort of make it work, but being able to set the properties with just a few `flex flex-column flex-*` attributes made it faster. Getting that coding live-reloading in my browser as I made mistakes was the best interactive, REPL-like experience I've had to gain an intuitive understanding of the new CSS layout options. For that, Tailwind was invaluable.

# Tailwind as Macro Language

It certainly is a lot less work to type `border-1` than `border-width: 1px; border-style: solid;`. This, I think, along with [popular UI tricks like blurred, semitransparent elements being baked in as simple attributes](https://tailwindcss.com/docs/backdrop-filter-blur) are the killer feature of Tailwind.

# Reining in the Complexity: Style Reuse

When I wanted a button-like element, I found myself going through a series of stages:

1. Style a single JSX component as-is with individual tailwind styles iteratively until I get to something that I like
1. Start on a second component that I want to make look similar to it
1. Copy/paste the style
1. Eventually I want to do a refresh system wide, so I find all the overlapping classes, cut them out and reuse them in backticked strings; I have something like

```typescript
export const TEXT_BUTTON =
  "font-normal rounded-lg bg-neutral-100 dark:bg-neutral-500 p-2 text-xs border-neutral-300 border disabled:text-neutral-300 dark:text-neutral-100 dark:bg-neutral-600 cursor-pointer";
```

And then custom elements that further refine the style:

```javascript
<span
  class={`${TEXT_BUTTON} rounded-l-none border-l-0 empty:hidden`}
  onClick={(e) => BlinkElement(e.target)}
>
  {children}
</span>
```

I think this is where I begin to stray from the way most people use Tailwind: I have a tendency to write lots of very small components and I am a bikeshedder in my visual styles so keeping all the elements in sync requires the type of DRY the `"tailwind attribute soup"` on every tag makes difficult.

# A Winning Combination: `@apply` and Vanilla CSS

Eventually I find myself wanting a `styles.css` having a `.button` class with all the inline constants pulled out. For the sake of readability and some light DRY, I'd rather my buttons be `<button className="button button-specialization">...` than ` <button className={``${TEXT_BUTTON} spec-1-attr spec-2-attr spec-3-attr``}>...`; I then find myself doing this:

```css
.button {
  @apply font-normal rounded-lg bg-neutral-100 dark:bg-neutral-500 p-2 text-xs border-neutral-300 border disabled:text-neutral-300 dark:text-neutral-100 dark:bg-neutral-600 cursor-pointer;
}

.button-specialization {
  @apply rounded-l-none border-l-0 empty:hidden;
}
```

That is; [the @apply directive](https://tailwindcss.com/docs/functions-and-directives#apply-directive) gives me Tailwind-style class macros in my CSS.

I can now use a more traditional approach to CSS: rather than a blast of appearance-based attributes on an element I can give it a semantic role which has an associated set of visual properties attributed to it.

I also needed this because I wanted to do some things with nested selectors that Tailwind did not entirely make possible (or at least easy). I found in places where it _could_ do selectors the shortened Tailwind attrs beyond `:has` and `:not` were harder to skim than fully-expressed CSS versions.

Anyway, `@apply` is awesome and I don't see its use encouraged much in the literature I've seen online. There are probably pedantic reasons for it that are all very reasonable but don't work for me. This worked for me.

# Burning the Ships

And, once I am happy with the style and relatively certain they won't change much going forward, I transform the core CSS with `@apply`d styles to fully expanded CSS and cut out Tailwind as a build time dependency. I have used Tailwind as a way to bootstrap my design system, and then cut it out of my build when it has overstayed its welcome.

# That's All

So that has been my last two years with Tailwind. I like it, it helped me get back up to speed with modern CSS and get a working visual prototype out the door quickly, I got tired of its class soup usage pattern, and I found that once I returned to old-fashioned CSS classes I could wean myself off it.
