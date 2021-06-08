#!/usr/bin/env bash

function vinyl() {
    cd ~/Documents/Computing/webscraper/scripts/
    conda activate web_s
    python vinyl_webscraper_urllist.py
    osascript -e 'quit app "Chrome"'
}
