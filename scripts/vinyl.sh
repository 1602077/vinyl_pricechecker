#!/usr/bin/env bash

function vinyl() {
    cd ~/Documents/Computing/webscraper/scripts/
    conda activate web_s
    python3 webscraper.py
    osascript -e 'quit app "Chrome"'
}
