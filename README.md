
# Discord-data Analyzer

A Python script to analyze the data discord collects about you and your usage behavior.

## How to use the tool?

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
