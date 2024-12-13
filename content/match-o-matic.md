+++
title =  "Match-O-Matic"
tags = ["toys"]
featured_image = ""
description = "Scrabble etc. cheater"
+++

This is a small toy for figuring out what to do with a set of letters. Use `_` as a wildcard.

{{< raw >}}
    <script>
      const rootWordNode = [
        0,
        {
          h: [0, { a: [0, { m: [1] }] }],
          c: [
            0,
            {
              h: [
                0,
                {
                  e: [0, { e: [0, { s: [0, { e: [1] }] }] }],
                  i: [0, { c: [0, { k: [0, { e: [0, { n: [1] }] }] }] }],
                },
              ],
            },
          ],
          s: [
            0,
            {
              a: [
                0,
                {
                  n: [
                    0,
                    { d: [0, { w: [0, { i: [0, { c: [0, { h: [1] }] }] }] }] },
                  ],
                },
              ],
            },
          ],
          b: [0, { r: [0, { e: [0, { a: [0, { d: [1] }] }] }] }],
        },
      ];

      let generation = 0;

      const letterCombination = function* (wordList) {
        const wl = Array.from(wordList);
        const visited = new Set();

        for (const index in wl) {
          const item = wl[index];
          if (visited.has(item)) {
            continue;
          }
          visited.add(item);
          const listCopy = [...wl];
          listCopy.splice(index, 1);

          yield [item, listCopy];
        }
      };

      const calculatePossibilities = (
        letterList,
        allLengthPossibilities = true
      ) => {
        const gen = generation;
        const words = [];
        const visited = new Set();

        const startTime = Date.now();
        const nodes = [["", letterList, rootWordNode]];
        while (nodes.length > 0) {
          const [wordSoFar, lettersLeft, node] = nodes.shift();
          const [isTerminal, childMap] = node;

          if (
            isTerminal &&
            (allLengthPossibilities || lettersLeft.length === 0)
          ) {
            if (!visited.has(wordSoFar)) {
              words.unshift(wordSoFar);
              visited.add(wordSoFar);
            }
          }

          for (const combo of letterCombination(lettersLeft)) {
            const [letter, letters] = combo;
            if (childMap === undefined) {
            } else if (childMap[letter] !== undefined) {
              nodes.push([wordSoFar + letter, letters, childMap[letter]]);
            } else if (letter === "_") {
              for (const [innerletter, innernode] of Object.entries(childMap)) {
                nodes.push([wordSoFar + innerletter, letters, innernode]);
              }
            }

            if (Date.now() - startTime > 250 || generation !== gen) {
              return words;
            }
          }
        }

        return words;
      };

      const debounce = (func, delay) => {
        let timeoutId;

        return function (...args) {
          clearTimeout(timeoutId);

          timeoutId = setTimeout(() => {
            func.apply(this, args);
          }, delay);
        };
      };

      const setItems = (itemList) => {
        const resultElt = document.getElementById("results");
        resultElt.innerText = null;

        for (const word of itemList) {
          const elt = document.createElement("div");
          elt.classList.add("match-o-matic-result");
          elt.innerText = word;
          resultElt.appendChild(elt);
        }

        if (itemList.length === 0) {
          const elt = document.createElement("div");
          elt.classList.add("match-o-matic-message");
          elt.innerText = "Nothing found";
          resultElt.appendChild(elt);
        }
      };

      const populatePossbilities = (valueString, matchLength) => {
        const resultElt = document.getElementById("results");
        resultElt.innerText = "Thinking";

        setItems(
          calculatePossibilities(valueString.toLowerCase(), matchLength)
        );
      };

      let matchLength = false;

      const updateValue = (e) => {
        const str = e.target.value;
        generation += 1;
        if (generation > 1000) {
          generation = 0;
        }

        populatePossbilities(str, matchLength);
      };

      const bind = () => {
        const inputElt = document.getElementById("textinput");
        inputElt.addEventListener("input", debounce(updateValue, 250));

        const matchlengthCheck = document.getElementById("matchlength");
        matchlengthCheck.checked = !matchLength;
        matchlengthCheck.addEventListener("change", (e) => {
          matchLength = !e.target.checked;
          populatePossbilities(inputElt.value, matchLength);
        });
      };

      document.addEventListener("DOMContentLoaded", bind);
    </script>
    <style type="text/css">
      .match-o-matic {
        margin-top: 12px;
        border: 1px solid rgba(0, 0, 0, 0.25);
        border-radius: 4px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 4px;
        background: white;
        color: black;
      }

      .match-o-matic-input-area {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        margin: 8px;
      }

      .match-o-matic-input {
        margin: 4px;
        padding: 4px;
        border: none;
        border-radius: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.25);
        font-size: xx-large;
        flex-grow: 1;
      }

      .match-o-matic-results {
        margin-top: 4px;
        border: 1px solid rgba(0, 0, 0, 0.125);
        border-radius: 4px;
        flex-grow: 1;
        font-size: large;
        padding: 4px;
      }

      .match-o-matic-results:empty {
        display: none;
      }

      .match-o-matic-results div + div {
        border-top: 1px solid rgba(0, 0, 0, 0.125);
      }

      .match-o-matic-result {
        font-size: x-large;
        padding: 4px;
        user-select: all;
      }

      .match-o-matic-message {
        text-align: center;
        padding: 16px;
        font-family: sans-serif;
      }

      @media only screen and (max-width: 800px) {
        .match-o-matic-input-area {
          flex-direction: column;
        }

        .match-o-matic-input {
          align-self: stretch;
          font-size: xx-large;
        }
      }
    </style>
    <div class="match-o-matic">
      <div class="match-o-matic-input-area">
        <input
          class="match-o-matic-input"
          placeholder="Type in letters here"
          type="text"
          id="textinput"
        />
        <label><input type="checkbox" id="matchlength" />Match length</label>
      </div>
      <div class="match-o-matic-results" id="results"></div>
    </div>
  {{< /raw >}}