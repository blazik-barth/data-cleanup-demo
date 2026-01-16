# Data Cleanup and Validation Automation Demo

## Overview
This Python demo script automatically cleans and validates CSV data according to pre-defined rules.

## Problem
Raw CSV data may often contain issues such as missing fields, inconsistent data formats, and duplicate entries, 
which can require a lot of time to manually clean up.

## Solution
This script takes as an input some CSV data. 
There is some sample data included in the system, but optionally, 
you can input an external CSV file as an argument to the script using the --in flag.
The script will look through the data and remove any entries that violate the given ruleset described below.
The script then outputs the newly cleaned data, as well as a summary of the cleanup process.

## Validation Rules
- Required fields: customer_id, email, signup_date
- Remove exact duplicate rows
- Validate email format
- Normalize signup dates to YYYY-MM-DD
- Drop invalid records, log results

## How To Run
```bash
pip install pandas
python clean_data.py
```

## Arguments
- --data: Specify which of two sample datasets should be cleaned with this program, "small" or "large". Default is "small".
```bash
python clean_data.py --data large
```
- --file: Specify the path to a custom CSV file to clean.
```bash
python clean_data.py --file path/to/custom.csv
```
If data and file are both specified, file will take priority.