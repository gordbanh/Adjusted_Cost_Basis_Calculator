# Adjusted Cost Basis Calculator
#### Video Demo: https://youtu.be/42EB041_mXM

## What will this script do?
This software is able to read your account activity from a CSV that you download from Questrade. Afterwards, it will compile the activity from each of your individual accounts and print out an aggregated pivot table showcasing each account #, the type of account, the account's holdings, in each currency purchased, quantity of shares still held, the net amount paid for all the shares, and finally the adjusted cost basis. This data is formatted to be readable for the average user. Optionally, the user can specify whether they would like the data exported into an xlsx with a name of their choosing (default is "Adjusted Cost Basis.xlsx") or the space between the columns of the printout.

## What are the inputs into this script?

### Required libraries:
- pandas
- numpy
- openpyxl
- argparse
- functools

### Positional arguments:
 - filename
   - filepath to csv input file

### Optional arguments:
 - -h, --help
   - Show this help message and exit
 - -c CSV, --csv CSV
   - If True, prints to xlsx
   - Default is False
 - -n NAME, --name NAME
   - Specify the name of the output xlsx file
   - Default is "Adjusted_Cost_Basis.xlsx"
 - -s SPACE, --space SPACE
   - Specify the space between the columns of the printed pivot table
   - Default is 3

## Why did you make this script?
I made this script to automate the process, gain new skills, as well as solve my own problem.

### The problem:
I hold my own portfolio of stocks in taxable accounts and will need to know and calculate the Adjusted Cost Basis in order to work out the Capital Gains. By doing some research, I found that the manual calculation was relatively slow, and some automated options were paid.

### Skills and learnings:
I would count myself as an "Excel Wizard" but still am relatively new to programming. I had previously done freeCodeCamp's "Relational Databases" and "Data Analysis with Python" courses and found it really helpful. I wanted to refresh and build those skills to memory, thus I utilized python and pandas to process this data. I also was able to utilize knowledge from Lecture 9, where I used "argparse" to generate positional and optional arguments. To regiment good practice, I also documented my code in Docstring format.

## What is some improvements or future work for this script?
Some future work that I would like to do is build upon the acceptable csv files that this script would take in. I only have accounts within Questrade, so I am unfamiliar with the formatting of other financial institutions. Also, this could be integrated into a tax calculator to find the total tax on your capital gain.
