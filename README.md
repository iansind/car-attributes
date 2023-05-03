# car-attributes

Web scraper that generates a dataset of car specs using caranddriver.com. Initially, a list of all available makes and models is generated in 'makes_models_scraper.py'. The main file then uses this list to scrape all available and desired spec data from the webpage of each make/model/style/trim combination. The most recent year is used for all vehicles, though this could be changed if desired.

The main file takes quite a long time to run due to the requested web crawler 10 second delay, so the scraping can be broken into chunks or run in the background. Expected total runtime is on the order of 15 hours, with large error bars. Checkpoints are made at regular intervals to ensure data is saved if there is any issue with connection. 

The web scraper is complete and functional, but the analysis is a work in progress. 

In its current state, visualization can be drawn from the data, including the following representation of crash safety ratings.

![image](https://user-images.githubusercontent.com/108632228/235813342-52cd2620-a6d8-4c74-9e76-9d9cabe9438b.png)

And the following representation of CO<sub>2</sub> emissions as they related to the price of the vehicle. 

![image](https://user-images.githubusercontent.com/108632228/235814387-71755bda-be85-4e1d-8e71-f68b508a7a35.png)
