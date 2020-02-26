# Farmers_Market_Forecasting

This project is focused on predicting weekly sales for a series of Farmer's Markets in Santa Monica that collectively handle ~$10 million in transactions annually. There are four separate markets that were studied that occur on different days of the week and have vendors of different varieties.

Using sales data for the market acquired from a Los Angeles market managing organization, I created forecasting model for each market, and specifically, for vendors of different varieties within each market (agricultural, baked goods, hot food, etc.)

The features my forecasting models are extracted from weather, city public information, google trends, and market metadata datasets. My models have an average mean average percent sales prediction error of 11.7%, as compared to a rough baseline of 14.3% for methods vendors are currently using.

The enhanced forecasting provided may the model can help vendors minimize product waste by more efficiently handling stocking and also may be used to guide dynamic pricing of produce on low-attendance market days.

The sales data is private and is not directly available on this repository but the databases utilized for feature extraction can be made available by request.

The app can be accessed at: http://www.seedforecasts.com/
