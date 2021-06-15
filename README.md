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

Adding this script to my shell profile file (```.zshrc``` in my case) with ```source ~/viny.sh``` allows me to run my script by simply typing ```vinyl``` into a terminal shell. If you are running a unix based system then this can be scheduled using ```crontab```.

Type ```crontab -e``` to open the crontab editor adding the following will cue the script to run at 6AM every day:
```
* 6 * * * export DISPLAY:=0; cd ~/.scripts; bash vinyl.sh
```
Full documentation on the ```crontab``` syntax can be found [here](https://man7.org/linux/man-pages/man5/crontab.5.html), while [crontab.guru](https://crontab.guru) is a useful tool for generating ```cron``` expressions if you are new to the tool. 

### TODOS
- [ ] Helper Functions
  - [ ] Remove record from wishlist (ideally by user inputing record title and this is removed from all output files and the url from the input file)
  - [ ] Plotting function - allow a user to specify one or more records and plot the history of their prices
- [ ] Update readme to reflect updates to scripts functionality, this should include all the function doc strings
- [ ] write a ```launchd``` plist to overcome issues with running cron and selenium
- [ ] document as to why you can't just run ```vinyl``` in ```cron```
