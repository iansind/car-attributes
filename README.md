# car-attributes

Web scraper that generates a dataset of car specs using caranddriver.com. Initially, a list of all available makes and models is generated in 'makes_models_scraper.py'. The main file then uses this list to scrape all available and desired spec data from the webpage of each make/model/style/trim combination. The most recent year is used for all vehicles, though this could be changed if desired.

The main file takes quite a long time to run due to the requested web crawler 10 second delay, so the scraping can be broken into chunks or run in the background. Expected total runtime is on the order of 15 hours, with large error bars. Checkpoints are made at regular intervals to ensure data is saved if there is any issue with connection. 

Work in progress. 
