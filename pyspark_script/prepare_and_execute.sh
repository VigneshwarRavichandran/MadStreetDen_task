#!/usr/bin/env bash

cd pyspark_script
unzip womens-shoes-prices.zip
pip install -r requirements.txt
python importer.py
