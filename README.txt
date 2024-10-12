# This script scrapes the most recent 90-day-median prices for a list of items from https://warframe.market using the warframe.market API.
# This script was created by 1Xanaton4You on 28.09.2024
#
# I wrote this scrip to get a easier overview over the current prices on the warframe.market.
#
# How to use this script on first use:
# 1. On windows open a command prompt by typing cmd into the windows seach field.
# 2. Type in phyton and press enter to check if you have phyton installed on your system.
#    2a. If you do not get something like this {Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
#                                               Type "help", "copyright", "credits" or "license" for more information.}
#        you first have to install Phyton on your system (https://www.python.org/downloads/).
#    2b. If you have a Phyton version installed type exit() and press enter to leave the phyton prompt.
# 3. Alter the [Set this according to your needs] part of the sript according to your needs, or use the predefined lists.
# 4. Start the script by double klicking the WarframeMarketScraper.py 
# 5. Select if you want to scrape all defined item lists or select a specific list. Choose the list number, if you want to scrape a single list.
# 6. Wait for the results. You can save the scraped results in a CSV-file when the scraping is done, if you choose to do so.
#    The file will be created in the folder this script runs from.