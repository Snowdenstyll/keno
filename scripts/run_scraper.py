#!/usr/bin/env python3

# run_scripts.py

import subprocess

# Run script1.py
subprocess.run(["python", "./scripts/scraper/webscraper.py"])

# Run script2.py
subprocess.run(["python", "./scripts/scraper/cleandata.py"])