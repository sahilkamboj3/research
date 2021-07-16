#!/bin/bash

function run_set() {
    count=0
    while [ $count -le 2000 ] 
    do
        python scrape_lg_user.py
        count=$((count+10))
        echo -n "$count"
        sleep 15
    done
}

run_set
