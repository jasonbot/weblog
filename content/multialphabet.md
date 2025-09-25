+++
title =  "Multialphabet"
tags = ["toys"]
featured_image = ""
description = "Make the "
+++

There are so many tools to do this online and a lot of them are annoying or overed in ads or both.

{{< raw >}}
    <script>
      const debounce = (func, delay) => {
        let timeoutId;

        return function (...args) {
          clearTimeout(timeoutId);

          timeoutId = setTimeout(() => {
            func.apply(this, args);
          }, delay);
        };
      };

      const bind = () => {
        const inputElt = document.getElementById("multi-alphabet-input");
        inputElt.addEventListener("input", debounce(updateValue, 250));

        // On load
        populatePossbilities(inputElt.value, matchLength);
      };

      document.addEventListener("DOMContentLoaded", bind);
    </script>
    <style type="text/css"></style>
    <div class="multi-alphabet">
      <div class="multi-alphabet-input-area">
        <textarea
          class="multi-alphabet-input"
          placeholder="Type your text here"
          id="textinput"
        ></textarea>
      </div>
      <div class="multi-alphabet-results" id="results"></div>
    </div>
  {{< /raw >}}