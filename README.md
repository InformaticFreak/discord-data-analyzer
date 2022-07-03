
# Discord-data Analyzer

[![GitHub License](https://img.shields.io/github/license/informaticfreak/discord-data-analyzer)](LICENSE)&nbsp;
[![Python Version](https://img.shields.io/badge/python-3-blue)](https://www.python.org/downloads/)&nbsp;
[![CodeFactor](https://www.codefactor.io/repository/github/informaticfreak/discord-data-analyzer/badge)](https://www.codefactor.io/repository/github/informaticfreak/discord-data-analyzer)&nbsp;
![visitors](https://visitor-badge.laobi.icu/badge?page_id=informaticfreak/discord-data-analyzer)&nbsp;

A Python script to analyze the data discord collects about you and your usage behavior.

## Important note

Because your discord data contains a lot of private information, you should **never upload or share your data** anywhere or with anyone!
Instead, program your own application or download an open source one to analyze your data. So you can stay in control of it.

## How to use the tool?

>**Requesting a Copy of your Data:** https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data

1. download your data from discord
2. rename the `package.circ` file to `package.zip`
3. extract the zip-file
4. add the path to your package directory into the `config.json` file with the `package_directory` key
5. create a directory for the results
6. add this results path to the file `config.json`, but with the key `results_directory`
7. open a terminal inside the `src` folder and run `main.py`
8. wait or type in what the script asks you
9. explore the results

## Requirements

```cmd
pip install -r requirements.txt
```

## Advanced (if you have multiple packages)

1. add the string `{ID}` to the end of the paths of the `config.json` file; e.g. `path/to/your/package{ID}` and `path/to/your/results{ID}`
2. run `main.py` from a terminal and at this point (`advanced package prefix (or press enter): `) enter your id to specify your package
