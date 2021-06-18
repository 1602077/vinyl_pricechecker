# vinyl_pricechecker

```webscraper.py``` is a python based web scraper which uses BeautifulSoup and Selenium to scrape the artist name, record title and price of records list on amazon as specified by my wishlist (```url.txt```) - an input file which contains an amazon url per line. Also included is a simple bash script which can be used to automate the price checking in a unix shell.

## Setting up the environment
Setting up the environment with the required libraries can be easily achieved using ```conda``` as follows:
```
conda env create --name web_s
conda install -n web_s pandas selenium BeautifulSoup matplotlib seaborn
```

The environment is activated by running ```conda activate web_s```.

If you do not have anaconda installed, you can install a lightweight distribution ([miniconda](https://docs.conda.io/en/latest/miniconda.html)) as follows with brew:
```brew install --cask anaconda```.
Alternatively, you may prefer to use the standard python ```venv``` along with ```pip```.


## Web scraping function
The main body of the scraping is performed by ```records_wishlist_scraper```, below I provide it's doc string which gives a brief overview of how it works.
```
records_wishlist_scraper(driver, url, price_only=False)

Web scraper to scrape the artist name, record title and current price for a given record as listed on amazon
specified by the url.
params:
------------------------------------------------------------------------------------------------------------
driver:         Selenium instance of the driver for the browser being used to perform the web scraping
                e.g. driver = webdriver.Safari()
url:            Amazon url for a given record whose price you would like to keep track of
price_only:     Boolean, if True scraper only returns the price for the record as specified in url. This is
                useful for records already with historic price data as we already know the artist name,
                and record title associated with that given url.
returns:
------------------------------------------------------------------------------------------------------------
artist_name:    Name of artist for the record specified by the input url
record_name:    Title of record for the input url
price:          Current price of record_title

```

## Running as a bash script
This is likely a script which you would like to run fairly frequent to get an accurate reflection of pricing. We can greatly simplify the process using a bash script and then automate this to run at a set time or frequency using a job scheduler.

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

Adding this script to my shell profile file (```.zshrc``` in my case) with ```source ~/viny.sh``` allows me to run my script by simply typing ```vinyl``` into a terminal shell. If you are running a unix based system then this can be scheduled using ```crontab```.

Type ```crontab -e``` to open the crontab editor adding the following will cue the script to run at 6AM every day:
```
* 6 * * * export DISPLAY:=0; cd ~/.scripts; bash vinyl.sh
```
Full documentation on the ```crontab``` syntax can be found [here](https://man7.org/linux/man-pages/man5/crontab.5.html), while [crontab.guru](https://crontab.guru) is a useful tool for generating ```cron``` expressions if you are new to the tool. 

### TODOS
- [ ] Helper Functions
  - [ ] Remove record from wishlist func (ideally by user inputing record title and this is removed from all output files and the url from the input file)
  - [ ] Plotting func - allow a user to specify one or more records and plot the history of their prices
- [ ] Update readme to reflect updates to scripts functionality, this should include all the function doc strings
- [ ] write a ```launchd``` plist to overcome issues with running cron and selenium
- [ ] document as to why you can't just run ```vinyl``` in ```cron```
