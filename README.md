
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

## Advanced (if you have multiple packages)

1. add the string `{ID}` to the end of the paths of the `config.json` file; e.g. `path/to/your/package{ID}` and `path/to/your/results{ID}`
2. run `main.py` from a terminal and at this point (`advanced package prefix (or press enter): `) enter your id to specify your package
