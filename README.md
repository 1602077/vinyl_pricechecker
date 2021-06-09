# vinyl_pricechecker

vinyl_webscraper_urllist.py is a python based webscraper which uses BeautifulSoup and Selenium to scrape the artist name, record title and price of records list on amazon as specified by my wishlist (url.txt) - an input which contains an amazon url per line. Also include is a simple bash scrpit which can be used to automate the price checking in a unix shell.

# Setting up the environment
Setting up the environment can be easily achieved using conda and pip as follows:

# Running the bash scripts
Example bash script include in ```scripts/vinyl.sh```:
```
function vinyl() {
    cd ~/Documents/Computing/webscraper/scripts/
    conda activate web_s
    python vinyl_webscraper_urllist.py
    osascript -e 'quit app "Chrome"'
}
```

# TODOS
- Adjust scrapping function to have a price only option
- Impliment historical price tracking dataframe
- Develop helper functions to easily remove records from wishlist when purchased, ideally through the user specifiying the record title and the associated url being deleted
