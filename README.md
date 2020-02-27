# Farmers Market Forecasting

# Project Goal

Farmers markets generate over a billion dollars in sales annually in the US and also provide platforms for promoting community engagement, the support of local businesses, and environmentally friendly agriculture. 

There are many types of vendors who reside at farmers market, such as agricultural vendors, hot food vendors (think taco stands, creperies, etc.), baked good vendors, and more. Many consumers prefer farmers markets because of the freshness of their products; however, this freshness often also means that many of these products are highly perishable. 

If you are a vendor, you have to predict how much product to stock for an upcoming market, and if you guess wrong, you can potentially lose significant amounts of money in product waste, which hampers your bottom-line profits and ultimately your ability to provide your services to the farmers market community. 

To combat this issue, I would like to create a sales forecaster that can predict the amount of sales that will be generated at an upcoming market for vendors of particular types (agricultural, hot food, etc). The predictions from this forecaster could be used by vendors to make more intelligent stocking/staffing predictions. 

The web-app dashboard for my completed project, written in DASH, can be accessed here: http://www.seedforecasts.com/

# Target audience for project

This project is focused on predicting weekly sales for a series of Farmer's Markets in Santa Monica (SM) that collectively handle ~$10 million in transactions annually. There are four separate markets that were studied that occur on three different days of the week (Wed, Sat, Sun) and have vendors of different varieties.

The resulting online dashboard product would be used by vendors of the 4 studied SM markets. 

# Technical approach

For each market, I want to be able to predict the average sales that will be generated per vendor within a specific vendor category. To do this I will featurize each market and then feed these features into a ridge regression model that can be trained on previous sales data to predict future sales outcomes. 


![](/Plots/github_pipeline.PNG?raw=true) 

# Data Sources

**Sales data

The sales data for the markets were acquired from a Los Angeles market managing organization. The dataset included the total sales generated for each market on each market date, broken down by vendor type (agricultural, baked good, hot goods, etc.). I created a sales forecasting model for each market, and specifically, for each vendor type within each market. There are four separate markets that have the following vendor data available

Saturday Market - Agricultural <br/>
Pico Market (Saturday as well, different location) - Agricultural, Hot Food, Baked Good, Coffee <br/>
Sunday Market - Agricultural, Hot Food, Baked Good, Retail, Coffee <br/>
Wednesday Market - Agricultural <br/>

Not all of these vendors have perishable goods (i.e. retail), but I have the data so I will still construct models just to see if anything useful can be gleamed. 

The predictions for one of my models is plot against the actual sales for one particular market/vendor combo below. Here I trained my data on 4 years of sales information and then tested it on the most recent year of data. 

![](/Plots/sunday_ag.PNG?raw=true)

**Market features

The features included in my forecasting models are extracted from weather, city public information, google trends, and market metadata datasets. 

Here is a list of features that were extracted for each market broken down by data type

Google Trends - how often the term 'farmers market' was googled in Los Angeles prior to market date
                https://trends.google.com/trends/explore?date=today%205-y&geo=US-CA-803&q=farmers%20market <br/>
                how often the term 'farmers market' was googled in Los Angeles prior to market date
                https://trends.google.com/trends/explore?date=today%205-y&geo=US-CA-803&q=los%20angeles%20wildfire


                
Santa Monica Parking Dataset - how occupied the parking structures in downtown Santa Monica were before market days (gives an indication on if people are traveling or if foot traffic appears to be elevated/depressed for some reason prior to a market event)
https://data.smgov.net/Transportation/Parking-Lot-Counts/ng8m-khuz

Market metadata - I know the date of each market in my dataset. From the date, I can extract the proximity to major holidays/events (~10 holiday features total, Christmas, thanksgiving, Superbowl, etc.). I can also convert the month the market took place into a one-hot-encoded set of 12 indicator variables. This can help track seasonal effects that are important in the market, such as crop cycles, school schedules, travel patterns, etc. 

Weather data - The wind, temperature, and rain on a given market day as well as the amount of rain the day before the market: https://www.meteoblue.com/en/weather/week/santa-monica_united-states-of-america_5393212
                
# Brief result overview

My models have an average mean average percent sales prediction error of roughly ~11%, as compared to an estimated baseline of ~13% for methods vendors are currently using. Here is a breakdown of the mape, grouped by product type and vendor type

The enhanced forecasting provided by the models can help vendors minimize product waste by more efficiently handling stocking and also may be used to guide dynamic pricing of produce on low-attendance market days.

The sales data is private and is not directly available on this repository, but the databases utilized for feature extraction can be made available by request.

![](/Plots/mape_by_day.PNG?raw=true) | ![](/Plots/mape_by_product.PNG?raw=true) 
 


**Caveats/Future improvements**

To train my model, I used sales data for previous market days. When featurizing these market dates for inclusion in the model, I used historical weather data for the particular market date. However, when predicting future market sales, I will only have weather *forecasts* available, not the actual weather. This will add some uncertainty to the model. 

Further, the model would be most useful if it could predict sales for an individual vendor rather than the average sales per vendors across a particular vendor class. Currently, the sales data for each vendor type is aggregated. The agency I partnered with can deaggregate the information so individual vendor sales, and even individual item sales for each vendor, are discernable. If I pursue the project further, these are avenues I would like to explore. 


# Organization of repo


All analysis was conducted in Python and SQL.
A brief overview of the repo structure is given here but please see each individual folder for more file details. 

Jupyter notebooks that were used for various aspects of the project (model evaluation, model construction, feature extraction, etc) are labeled and stored in the 'Notebooks' folder. 

The total feature matrix is included in the 'Feature_Data_Files' folder as well as other scraped (Google Trends, etc.) data sets. 

The results of the models and the models themselves are stored in separate files for each vendor/product combination in the 'Model_Files' folder. 

The assets folder contains the DASH dashboard style files, the weather folder contains the raw/cleaned weather data, and the Dashboard.py while contains the code for the online interface.





