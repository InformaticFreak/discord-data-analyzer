
# Discord-data Analyzer

[![GitHub License](https://img.shields.io/github/license/informaticfreak/Discord-data-analyzer)](LICENSE)&nbsp;
[![Python Version](https://img.shields.io/badge/python-3-blue)](https://www.python.org/downloads/)&nbsp;
[![CodeFactor](https://www.codefactor.io/repository/github/informaticfreak/Discord-data-analyzer/badge)](https://www.codefactor.io/repository/github/informaticfreak/Discord-data-analyzer)&nbsp;
![visitors](https://visitor-badge.laobi.icu/badge?page_id=informaticfreak/Discord-data-analyzer)&nbsp;

A Python script to analyze the data Discord collects about you and your usage behavior.

>**Requesting a Copy of your Data:**
>
>https://support.Discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data

## Important note

Because your Discord data contains a lot of private information, you should **never upload or share your data** anywhere or with anyone!
Instead, program your own application or download an open source one to analyze your data. So you can stay in control of it.

## How to use the tool?

1. download your data from Discord
2. if not, rename the downloaded file to `package.zip`
3. extract the zip-file
4. add the path to your package directory into the `config.json` file with the `package_directory` key
5. create a directory for the results
6. add this results path to the file `config.json`, but with the key `results_directory`
7. open a terminal inside the `src` folder and run `src/main.py`
8. wait or type in what the script asks you
9. explore the results

## Requirements

```cmd
pip install -r requirements.txt
```

## Advanced (if you have multiple packages)

1. add the string `{ID}` to the end of the paths of the `config.json` file; e.g. `path/to/your/package{ID}` and `path/to/your/results{ID}`
2. run `src/main.py` from a terminal and at this point (`advanced package prefix (or press enter): `) enter your id to specify your package
