# vinyl_pricechecker

```webscraper.py``` is a python based web scraper which uses BeautifulSoup and Selenium to scrape the artist name, record title and price of records list on amazon as specified by my wishlist (```url.txt```) - an input file which contains an amazon url per line. Also included is a simple bash script which can be used to automate the price checking in a unix shell.

# Setting up the environment
Setting up the environment with the required libraries can be easily achieved using ```conda``` as follows:
```
conda env create --name web_s
conda install -n web_s pandas selenium BeautifulSoup
```

The environment is activated by running ```conda activate web_s```.

If you do not have anaconda installed, you can install a lightweight distribution ([miniconda](https://docs.conda.io/en/latest/miniconda.html)) as follows with brew:
```brew install --cask anaconda```.
Alternatively, you may prefer to use the standard python ```venv``` along with ```pip```.

# Running as a bash script
Example bash script included in ```scripts/vinyl.sh```:
```
function vinyl() {
    cd ~/Documents/Computing/webscraper/scripts/
    conda activate web_s
    python3 webscraper.py
    osascript -e 'quit app "Chrome"'
}
```
If you are using the webscraper in chrome you may want to consider adding the following ```osascript -e 'quit app "Chrome"'```, which will ensure that all chrome threads are terminated after the script has finished executing.

### TODOS
- [x] Adjust scrapping function to have a price only option
- [x] Implement historical price tracking data frame
- [ ] Develop helper functions to easily remove records from wishlist when purchased, ideally through the user specifying the record title and the associated url being deleted
- [x] Output a second df with the best price previous and current price stats
- [ ] Adding a plotter helper function so that user's can input several records price to track and plot historical data
- [ ] Update readme to reflect updates to scripts functionality, this should include all the function doc strings
