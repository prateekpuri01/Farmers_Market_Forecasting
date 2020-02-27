# Farmers_Market_Forecasting

**Project Goal**

Farmers markets generate over a billion dollars in sales annually and also provide platforms for promoting community engagement, the support of local businesses, and environmentally-friendly agriculture. 

There are many types of vendors who reside at farmers market, such as agricultural vendors, hot food vendors (think taco stand, crepes, etc), baked good vendors, and more. In fact, many consumers prefer farmers markets because of the freshness of these products; however, this freshness often also means that many of these products are perishable. 

If you are a vendor, you have to predict how much product to stock for an upcoming market, and if you guess wrong, you can potentially lose significant amounts of money in product waste, which hampers your bottom-line profits and ultimately your ability to provide your services to the farmers market community. 

To combat this issue, I would like to create a sales forecaster that can predict the amount of sales that will be generated at an upcoming market for vendors of particular types (agricultural, hot food, etc). The predicitons from this forecaster could be used by vendors to make more intelligent stocking/staffind predictions. 

**Domain of project**

This project is focused on predicting weekly sales for a series of Farmer's Markets in Santa Monica that collectively handle ~$10 million in transactions annually. There are four separate markets that were studied that occur on three different days of the week (Wed, Sat, Sun) and have vendors of different varieties.

**Technical approach**

For each market, I want to be able to predict the average sales that will be generated per vendor within a specific vendor categroy. To do this I will featurize each market and then feed these features into a ridge regression model that can be trained on previous sales data to predict future sales outcomes. 

**Data Sources**

*Sales data*

The sales data for the markets weere acquired from a Los Angeles market managing organization. The dataset included the total sales generated for each market on each market date, broken down by vendor type (agricultural, baked good, hot goods, etc.). I created a sales forecasting model for each market, and specifically, for each vendors type within each market.

*Market features*

The features included in my forecasting models are extracted from weather, city public information, google trends, and market metadata datasets. 

Here is a list of features that were extracted for each market broken down by data type

Google Trends - how often the term 'farmers market' was googled in Los Angeles prior to market date
                https://trends.google.com/trends/explore?date=today%205-y&geo=US-CA-803&q=farmers%20market

                how often the term 'los angeles wildfire' was googled in Los Angeles prior to market date
                https://trends.google.com/trends/explore?date=today%205-y&geo=US-CA-803&q=los%20angeles%20wildfire
                
Santa Monica Parking Dataset - how occuiped the parking structures in downtown santa monica were before market days (gives an indiciation on if people are traveling or if foot traffic appears to be elevated/depressed for some reason prior to a market event)
https://data.smgov.net/Transportation/Parking-Lot-Counts/ng8m-khuz

Market metadata - I know the date of each market in my dataset. Fromt the date, I can extract the proximity to major holidays/events (~10 holiday features total, christmas, thanksgiving, superbowl, etc.). I can also convert the month the market took place into a one-hot-encoded set of 12 indicator variables. This can help track seasonal effects that are important in the market, such as crop cycles, school schedules, travel patterns, etc. 
                

My models have an average mean average percent sales prediction error of 11.7%, as compared to a rough baseline of 14.3% for methods vendors are currently using.

The enhanced forecasting provided by the models can help vendors minimize product waste by more efficiently handling stocking and also may be used to guide dynamic pricing of produce on low-attendance market days.

The sales data is private and is not directly available on this repository but the databases utilized for feature extraction can be made available by request.

The dashbaord, constructed in python DASH, can be accessed at: http://www.seedforecasts.com/
