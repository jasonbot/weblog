+++
title =  "Multialphabet"
tags = ["toys"]
featured_image = ""
description = "Make the "
+++

There are so many tools to do this online and a lot of them are annoying or covered in ads or both. Type text, get transforms.

{{< raw >}}
    <script>
      const randomChoice = (array) =>
        array[Math.floor(Math.random() * array.length)];

      const plainAlphabetMapping = (...alphabetString) => {
        return (mappingString) =>
          [
            ...(mappingString.length === 0
              ? randomChoice([
                  "We hold these truths to be self-evident, that all men are created equal, that they are endowed by their Creator with certain unalienable Rights, that among these are Life, Liberty and the pursuit of Happiness.",
                  "Whereas recognition of the inherent dignity and of the equal and inalienable rights of all members of the human family is the foundation of freedom, justice and peace in the world,",
                  "Space: the final frontier. These are the voyages of the starship Enterprise. Its continuing mission: to explore strange new worlds, to seek out new life and new civilizations, to boldly go where no man has gone before",
                  `So, I want you to get up now. I want all of you to get up out of your chairs. I want you to get up right now and go to the window, open it, and stick your head out and yell, "I'm as mad as hell, and I'm not going to take this anymore!!"`,
                  "Hello from the children of planet Earth.",
                  `I know how hard it is down in Chino
I know how you struggle just to get by
I know they got farm fresh eggs down in Chino
And tract homes reasonably priced`,
                ])
              : mappingString),
          ]
            .map((letter, i) => {
              const charCode = letter.charCodeAt(0);
              if (charCode >= 65 && charCode <= 91) {
                return alphabetString[charCode - 65] ?? letter;
              }
              if (charCode >= 97 && charCode <= 123) {
                return alphabetString[charCode - 97 + 26] ?? letter;
              }

              return letter;
            })
            .join("");
      };

      const translators = {
        Bold: plainAlphabetMapping(
          "𝐀",
          "𝐁",
          "𝐂",
          "𝐃",
          "𝐄",
          "𝐅",
          "𝐆",
          "𝐇",
          "𝐈",
          "𝐉",
          "𝐊",
          "𝐋",
          "𝐌",
          "𝐍",
          "𝐎",
          "𝐏",
          "𝐐",
          "𝐑",
          "𝐒",
          "𝐓",
          "𝐔",
          "𝐕",
          "𝐖",
          "𝐗",
          "𝐘",
          "𝐙",
          "𝐚",
          "𝐛",
          "𝐜",
          "𝐝",
          "𝐞",
          "𝐟",
          "𝐠",
          "𝐡",
          "𝐢",
          "𝐣",
          "𝐤",
          "𝐥",
          "𝐦",
          "𝐧",
          "𝐨",
          "𝐩",
          "𝐪",
          "𝐫",
          "𝐬",
          "𝐭",
          "𝐮",
          "𝐯",
          "𝐰",
          "𝐱",
          "𝐲",
          "𝐳"
        ),
        Italic: plainAlphabetMapping(
          "𝐴",
          "𝐵",
          "𝐶",
          "𝐷",
          "𝐸",
          "𝐹",
          "𝐺",
          "𝐻",
          "𝐼",
          "𝐽",
          "𝐾",
          "𝐿",
          "𝑀",
          "𝑁",
          "𝑂",
          "𝑃",
          "𝑄",
          "𝑅",
          "𝑆",
          "𝑇",
          "𝑈",
          "𝑉",
          "𝑊",
          "𝑋",
          "𝑌",
          "𝑍",
          "𝑎",
          "𝑏",
          "𝑐",
          "𝑑",
          "𝑒",
          "𝑓",
          "𝑔",
          "𝒉",
          "𝑖",
          "𝑗",
          "𝑘",
          "𝑙",
          "𝑚",
          "𝑛",
          "𝑜",
          "𝑝",
          "𝑞",
          "𝑟",
          "𝑠",
          "𝑡",
          "𝑢",
          "𝑣",
          "𝑤",
          "𝑥",
          "𝑦",
          "𝑧"
        ),
        "Bold Italic": plainAlphabetMapping(
          "𝑨",
          "𝑩",
          "𝑪",
          "𝑫",
          "𝑬",
          "𝑭",
          "𝑮",
          "𝑯",
          "𝑰",
          "𝑱",
          "𝑲",
          "𝑳",
          "𝑴",
          "𝑵",
          "𝑶",
          "𝑷",
          "𝑸",
          "𝑹",
          "𝑺",
          "𝑻",
          "𝑼",
          "𝑽",
          "𝑾",
          "𝑿",
          "𝒀",
          "𝒁",
          "𝒂",
          "𝒃",
          "𝒄",
          "𝒅",
          "𝒆",
          "𝒇",
          "𝒈",
          "𝒉",
          "𝒊",
          "𝒋",
          "𝒌",
          "𝒍",
          "𝒎",
          "𝒏",
          "𝒐",
          "𝒑",
          "𝒒",
          "𝒓",
          "𝒔",
          "𝒕",
          "𝒖",
          "𝒗",
          "𝒘",
          "𝒙",
          "𝒚",
          "𝒛"
        ),
        "Italic Cursive": plainAlphabetMapping(
          "𝒜",
          "𝓑",
          "𝒞",
          "𝒟",
          "𝓔",
          "𝓕",
          "𝒢",
          "𝓗",
          "I",
          "𝓘",
          "𝒥",
          "𝒦",
          "𝓛",
          "𝓜",
          "𝒩",
          "𝒪",
          "𝒫",
          "𝒬",
          "𝒮",
          "𝒯",
          "𝒰",
          "𝒱",
          "𝒲",
          "𝒳",
          "𝒴",
          "𝒵",
          "𝒶",
          "𝒷",
          "𝒸",
          "𝒹",
          "𝓮",
          "𝒻",
          "𝓰",
          "𝒽",
          "𝒾",
          "𝒿",
          "𝓀",
          "𝓁",
          "𝓂",
          "𝓃",
          "𝓸",
          "𝓅",
          "𝓆",
          "𝓇",
          "𝓈",
          "𝓉",
          "𝓊",
          "𝓋",
          "𝓌",
          "𝓍",
          "𝓎",
          "𝓏"
        ),
        "Bold Italic Cursive": plainAlphabetMapping(
          "𝓐",
          "𝓑",
          "𝓒",
          "𝓓",
          "𝓔",
          "𝓕",
          "𝓖",
          "𝓗",
          "𝓘",
          "𝓙",
          "𝓚",
          "𝓛",
          "𝓜",
          "𝓝",
          "𝓞",
          "𝓟",
          "𝓠",
          "𝓡",
          "𝓢",
          "𝓣",
          "𝓤",
          "𝓥",
          "𝓦",
          "𝓧",
          "𝓨",
          "𝓩",
          "𝓪",
          "𝓫",
          "𝓬",
          "𝓭",
          "𝓮",
          "𝓯",
          "𝓰",
          "𝓱",
          "𝓲",
          "𝓳",
          "𝓴",
          "𝓵",
          "𝓶",
          "𝓷",
          "𝓸",
          "𝓹",
          "𝓺",
          "𝓻",
          "𝓼",
          "𝓽",
          "𝓾",
          "𝓿",
          "𝔀",
          "𝔁",
          "𝔂",
          "𝔃"
        ),
        Fraktur: plainAlphabetMapping(
          "𝔄",
          "𝔅",
          "𝕮",
          "𝔇",
          "𝔈",
          "𝔉",
          "𝔊",
          "𝕳",
          "𝕴",
          "𝔍",
          "𝔎",
          "𝔏",
          "𝔐",
          "𝔑",
          "𝔒",
          "𝔓",
          "𝔔",
          "𝕽",
          "𝔖",
          "𝔗",
          "𝔘",
          "𝔙",
          "𝔚",
          "𝔛",
          "𝔜",
          "Z",
          "𝔞",
          "𝔟",
          "𝔠",
          "𝔡",
          "𝔢",
          "𝔣",
          "𝔤",
          "𝔥",
          "𝔦",
          "𝔧",
          "𝔨",
          "𝔩",
          "𝔪",
          "𝔫",
          "𝔬",
          "𝔭",
          "𝔮",
          "𝔯",
          "𝔰",
          "𝔱",
          "𝔲",
          "𝔳",
          "𝔴",
          "𝔵",
          "𝔶",
          "𝔷"
        ),
        "Bold Fraktur": plainAlphabetMapping(
          "𝕬",
          "𝕭",
          "𝕮",
          "𝕯",
          "𝕰",
          "𝕱",
          "𝕲",
          "𝕳",
          "𝕴",
          "𝕵",
          "𝕶",
          "𝕷",
          "𝕸",
          "𝕹",
          "𝕺",
          "𝕻",
          "𝕼",
          "𝕽",
          "𝕾",
          "𝕿",
          "𝖀",
          "𝖁",
          "𝖂",
          "𝖃",
          "𝖄",
          "𝖅",
          "𝖆",
          "𝖇",
          "𝖈",
          "𝖉",
          "𝖊",
          "𝖋",
          "𝖌",
          "𝖍",
          "𝖎",
          "𝖏",
          "𝖐",
          "𝖑",
          "𝖒",
          "𝖓",
          "𝖔",
          "𝖕",
          "𝖖",
          "𝖗",
          "𝖘",
          "𝖙",
          "𝖚",
          "𝖛",
          "𝖜",
          "𝖝",
          "𝖞",
          "𝖟"
        ),
        Draftsman: plainAlphabetMapping(
          "𝔸",
          "𝔹",
          "C",
          "𝔻",
          "𝔼",
          "𝔽",
          "𝔾",
          "H",
          "𝕀",
          "𝕁",
          "𝕂",
          "𝕃",
          "𝕄",
          "N",
          "𝕆",
          "P",
          "Q",
          "R",
          "𝕊",
          "𝕋",
          "𝕌",
          "𝕍",
          "𝕎",
          "𝕏",
          "𝕐",
          "Z",
          "𝕒",
          "𝕓",
          "𝕔",
          "𝕕",
          "𝕖",
          "𝕗",
          "𝕘",
          "𝕙",
          "𝕚",
          "𝕛",
          "𝕜",
          "𝕝",
          "𝕞",
          "𝕟",
          "𝕠",
          "𝕡",
          "𝕢",
          "𝕣",
          "𝕤",
          "𝕥",
          "𝕦",
          "𝕧",
          "𝕨",
          "𝕩",
          "𝕪",
          "𝕫"
        ),
        Wide: plainAlphabetMapping(
          "𝖠",
          "𝖡",
          "𝖢",
          "𝖣",
          "𝖤",
          "𝖥",
          "𝖦",
          "𝖧",
          "𝖨",
          "𝖩",
          "𝖪",
          "𝖫",
          "𝖬",
          "𝖭",
          "𝖮",
          "𝖯",
          "𝖰",
          "𝖱",
          "𝖲",
          "𝖳",
          "𝖴",
          "𝖵",
          "𝖶",
          "𝖷",
          "𝖸",
          "𝖹",
          "𝖺",
          "𝖻",
          "𝖼",
          "𝖽",
          "𝖾",
          "𝖿",
          "𝗀",
          "𝗁",
          "𝗂",
          "𝗃",
          "𝗄",
          "𝗅",
          "𝗆",
          "𝗇",
          "𝗈",
          "𝗉",
          "𝗊",
          "𝗋",
          "𝗌",
          "𝗍",
          "𝗎",
          "𝗏",
          "𝗐",
          "𝗑",
          "𝗒",
          "𝗓"
        ),
        "Bold Wide": plainAlphabetMapping(
          "𝗔",
          "𝗕",
          "𝗖",
          "𝗗",
          "𝗘",
          "𝗙",
          "𝗚",
          "𝗛",
          "𝗜",
          "𝗝",
          "𝗞",
          "𝗟",
          "𝗠",
          "𝗡",
          "𝗢",
          "𝗣",
          "𝗤",
          "𝗥",
          "𝗦",
          "𝗧",
          "𝗨",
          "𝗩",
          "𝗪",
          "𝗫",
          "𝗬",
          "𝗭",
          "𝗮",
          "𝗯",
          "𝗰",
          "𝗱",
          "𝗲",
          "𝗳",
          "𝗴",
          "𝗵",
          "𝗶",
          "𝗷",
          "𝗸",
          "𝗹",
          "𝗺",
          "𝗻",
          "𝗼",
          "𝗽",
          "𝗾",
          "𝗿",
          "𝘀",
          "𝘁",
          "𝘂",
          "𝘃",
          "𝘄",
          "𝘅",
          "𝘆",
          "𝘇"
        ),
        "Wide Italic": plainAlphabetMapping(
          "𝘈",
          "𝘉",
          "𝘊",
          "𝘋",
          "𝘌",
          "𝘍",
          "𝘎",
          "𝘏",
          "𝘐",
          "𝘑",
          "𝘒",
          "𝘓",
          "𝘔",
          "𝘕",
          "𝘖",
          "𝘗",
          "𝘘",
          "𝘙",
          "𝘚",
          "𝘛",
          "𝘜",
          "𝘝",
          "𝘞",
          "𝘟",
          "𝘠",
          "𝘡",
          "𝘢",
          "𝘣",
          "𝘤",
          "𝘥",
          "𝘦",
          "𝘧",
          "𝘨",
          "𝘩",
          "𝘪",
          "𝘫",
          "𝘬",
          "𝘭",
          "𝘮",
          "𝘯",
          "𝘰",
          "𝘱",
          "𝘲",
          "𝘳",
          "𝘴",
          "𝘵",
          "𝘶",
          "𝘷",
          "𝘸",
          "𝘹",
          "𝘺",
          "𝘻"
        ),
        "Bold Wide Italic": plainAlphabetMapping(
          "𝘼",
          "𝘽",
          "𝘾",
          "𝘿",
          "𝙀",
          "𝙁",
          "𝙂",
          "𝙃",
          "𝙄",
          "𝙅",
          "𝙆",
          "𝙇",
          "𝙈",
          "𝙉",
          "𝙊",
          "𝙋",
          "𝙌",
          "𝙍",
          "𝙎",
          "𝙏",
          "𝙐",
          "𝙑",
          "𝙒",
          "𝙓",
          "𝙔",
          "𝙕",
          "𝙖",
          "𝙗",
          "𝙘",
          "𝙙",
          "𝙚",
          "𝙛",
          "𝙜",
          "𝙝",
          "𝙞",
          "𝙟",
          "𝙠",
          "𝙡",
          "𝙢",
          "𝙣",
          "𝙤",
          "𝙥",
          "𝙦",
          "𝙧",
          "𝙨",
          "𝙩",
          "𝙪",
          "𝙫",
          "𝙬",
          "𝙭",
          "𝙮",
          "𝙯"
        ),
        Typewriter: plainAlphabetMapping(
          "𝙰",
          "𝙱",
          "𝙲",
          "𝙳",
          "𝙴",
          "𝙵",
          "𝙶",
          "𝙷",
          "𝙸",
          "𝙹",
          "𝙺",
          "𝙻",
          "𝙼",
          "𝙽",
          "𝙾",
          "𝙿",
          "𝚀",
          "𝚁",
          "𝚂",
          "𝚃",
          "𝚄",
          "𝚅",
          "𝚆",
          "𝚇",
          "𝚈",
          "𝚉",
          "𝚊",
          "𝚋",
          "𝚌",
          "𝚍",
          "𝚎",
          "𝚏",
          "𝚐",
          "𝚑",
          "𝚒",
          "𝚓",
          "𝚔",
          "𝚕",
          "𝚖",
          "𝚗",
          "𝚘",
          "𝚙",
          "𝚚",
          "𝚛",
          "𝚜",
          "𝚝",
          "𝚞",
          "𝚟",
          "𝚠",
          "𝚡",
          "𝚢",
          "𝚣"
        ),
        Doublewide: plainAlphabetMapping(
          "Ａ",
          "Ｂ",
          "Ｃ",
          "Ｄ",
          "Ｅ",
          "Ｆ",
          "Ｇ",
          "Ｈ",
          "Ｉ",
          "Ｊ",
          "Ｋ",
          "Ｌ",
          "Ｍ",
          "Ｎ",
          "Ｏ",
          "Ｐ",
          "Ｑ",
          "Ｒ",
          "Ｓ",
          "Ｔ",
          "Ｕ",
          "Ｖ",
          "Ｗ",
          "Ｘ",
          "Ｙ",
          "Ｚ",
          "ａ",
          "ｂ",
          "ｃ",
          "ｄ",
          "ｅ",
          "ｆ",
          "ｇ",
          "ｈ",
          "ｉ",
          "ｊ",
          "ｋ",
          "ｌ",
          "ｍ",
          "ｎ",
          "ｏ",
          "ｐ",
          "ｑ",
          "ｒ",
          "ｓ",
          "ｔ",
          "ｕ",
          "ｖ",
          "ｗ",
          "ｘ",
          "ｙ",
          "ｚ"
        ),
      };

      const activeTranslations = [];

      const debounce = (func, delay) => {
        let timeoutId;

        return function (...args) {
          clearTimeout(timeoutId);

          timeoutId = setTimeout(() => {
            func.apply(this, args);
          }, delay);
        };
      };

      const inputTextHasChanged = () => {
        const t = document.getElementById("multi-alphabet-input");
        const text = t.innerText;

        if (!!text && activeTranslations.length === 0) {
          addToListOfActiveTranslations(Object.keys(translators)[0]);
        }

        activeTranslations.forEach((display) => {
          display.update(text);
        });
      };

      const updateSelectedTranslationItemsInList = () => {
        namesUsed = new Set(activeTranslations.map((b) => b.name));

        const selectElt = document.getElementById("multi-alphabet-selector");
        [...selectElt.querySelectorAll("option")].forEach((e) => {
          e.disabled = namesUsed.has(e.value);
        });
        inputTextHasChanged();
      };

      const addToListOfActiveTranslations = (name) => {
        const template = document.getElementById("translation-item-template");
        const resultElt = document.getElementById("multi-alphabet-results");

        const translationElt = document.importNode(
          template.content,
          true
        ).firstElementChild;
        resultElt.appendChild(translationElt);

        translationElt.querySelector(
          ".name"
        ).innerText = `${name} (${translators[name](name)})`;

        const translationTextelt = translationElt.querySelector(".translation");
        const copyButton = translationElt.querySelector(".copy-button");
        const deleteButton = translationElt.querySelector(".remove-button");

        copyButton.addEventListener("click", (e) => {
          navigator.clipboard.writeText(translationTextelt.innerText);
        });

        deleteButton.addEventListener("click", (e) => {
          const idx = activeTranslations.indexOf((e) => e.name === name);
          activeTranslations.pop(idx);
          resultElt.removeChild(translationElt);
          updateSelectedTranslationItemsInList();
        });

        activeTranslations.push({
          name: name,
          update: (text) => {
            const translationBlank = text.trim().length === 0;
            copyButton.disabled = translationBlank;

            translationTextelt.innerText = translators[name](text);
          },
        });
        updateSelectedTranslationItemsInList();
      };

      const startupAndBindElements = () => {
        const selectElt = document.getElementById("multi-alphabet-selector");
        selectElt.addEventListener("change", (e) => {
          addToListOfActiveTranslations(e.target.value);
          selectElt.value = "";
        });

        Object.entries(translators).forEach(([name, translator]) => {
          const option = document.createElement("option");
          option.value = name;
          option.textContent = `${name} (${translator(name)})`;

          selectElt.appendChild(option);
        });

        const inputElt = document.getElementById("multi-alphabet-input");
        inputElt.addEventListener("input", debounce(inputTextHasChanged, 150));
      };

      document.addEventListener("DOMContentLoaded", startupAndBindElements);
    </script>
    <style type="text/css">
      div.multi-alphabet-input-area {
        border: 1px solid rgba(0, 0, 0, 0.125);
        border-radius: 4px;
        padding: 4px;
        font-size: larger;

        &:empty::before {
          content: "Type your dumb words here";
          opacity: 0.75;
          font-style: italic;
        }

        margin-bottom: 1em;
      }

      div.translation-item {
        border: 1px solid rgba(0, 0, 0, 0.125);
        border-radius: 4px;
      }

      div.translation-text {
        padding: 4px;
        white-space: pre-wrap;
        padding: 4px;
        font-size: larger;
      }

      div.translation-header {
        background-color: rgba(0, 0, 0, 0.075);
        padding: 2px;
        user-select: none;
        display: flex;
        flex-direction: row;

        .translator-name {
          text-align: center;
        }

        & > * {
          flex-grow: 1;
          align-items: center;
        }

        .copy-button,
        .remove-button {
          flex-grow: 0;
        }
      }

      div.multi-alphabet-add-another {
        select {
          font-size: large;
          font-weight: bold;
        }

        margin-top: 4px;
        margin-bottom: 4px;
        user-select: none;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-end;
      }

      div.translation-item:not(:last-child) {
        border-bottom: 1px solid rgba(0, 0, 0, 0.125);
        padding-bottom: 4px;
        margin-bottom: 4px;
      }
    </style>
    <div class="multi-alphabet">
      <div
        id="multi-alphabet-input"
        class="multi-alphabet-input-area"
        contenteditable="true"
      ></div>
      <div class="multi-alphabet-results" id="multi-alphabet-results"></div>
      <div class="multi-alphabet-add-another">
        <select
          class="multi-alphabet-translation-selector"
          id="multi-alphabet-selector"
        >
          <option disabled value="" selected>Add another:</option>
        </select>
      </div>

      <template id="translation-item-template">
        <div class="translation-item">
          <div class="translation-header">
            <div class="name translator-name"></div>
            <button class="copy-button">⧉Copy</button>
            <button class="remove-button">🗙</button>
          </div>
          <div class="translation translation-text"></div>
        </div>
      </template>
    </div>
  {{< /raw >}}
