import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import datetime
import math
import numpy as np
import holidays
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn import preprocessing
import pickle
from datetime import timedelta


def get_holidays(holiday_name,threeDay,holiday_name_observed=[]):
    hol_dates=[]
    for year in range(2013,2021):
        holiday_list=holidays.UnitedStates(years = year)
        for holiday in holiday_list.keys():
            if holiday_list[holiday]==holiday_name or holiday_list[holiday]==holiday_name_observed:
                hol_dates.append(holiday)
                if holiday.weekday()==0 and threeDay==1:
                    hol_dates.append(holiday-timedelta(days=1))
                    hol_dates.append(holiday-timedelta(days=2))
                elif holiday.weekday()==4 and threeDay==1:
                    hol_dates.append(holiday+timedelta(days=1))
                    hol_dates.append(holiday+timedelta(days=2))
    return hol_dates


NY=["New Year's Day"]
MLK=["Martin Luther King, Jr. Day"]
WASH=["Washington's Birthday"]
LABOR=["Labor Day"]
MEMORIAL=['Memorial Day']
J4=["Independence Day","Independence Day (Observed)"]
VET=['Veterans Day','Veterans Day (Observed)']
THANK=['Thanksgiving']

thanksgivings=get_holidays(THANK[0],1)+[x - timedelta(days=1) for x in get_holidays(THANK[0],1)]+[x + timedelta(days=3) for x in get_holidays(THANK[0],1)]+[x + timedelta(days=2) for x in get_holidays(THANK[0],1)]
NYE_dates=get_holidays(NY[0],1)+[x - timedelta(days=1) for x in get_holidays(NY[0],1)]
veterans_days=get_holidays(VET[0],1,VET[1])
mlk_days=get_holidays(MLK[0],1)
memorial_days=get_holidays(MEMORIAL[0],1)
wash_days=get_holidays(WASH[0],1)
labor_days=get_holidays(LABOR[0],1)
july_fourths=get_holidays(J4[0],1,J4[1])


weekday_dict={'WDT':(2,'Wednesday'),'SDT':(5,'Saturday'), 'PICO': (5,'Saturday'),'MAIN':(6,'Sunday')}




current_weather_info=pd.read_pickle('weather_scrape.pkl')
future_forecast_dates=list(current_weather_info[0].keys())
current_temp_info=current_weather_info[0]
current_rain_info=current_weather_info[1]
current_wind_info=current_weather_info[2]

def holiday_check(x,dates):
    if x.date() in dates:
        return 1
    else:
        return 0
    
def christmas_check(x):
    if x.month==12:
        if x.day>=19 and x.day<=25:
            return 1
        return 0
    return 0


superbowls=[datetime.date(2011,2,6),datetime.date(2012,2,5),datetime.date(2013,2,3),
            datetime.date(2014,2,2),datetime.date(2015,2,1),datetime.date(2016,2,7),
                datetime.date(2017,2,5),datetime.date(2018,2,4),datetime.date(2019,2,3)]
superbowls=superbowls+[x-timedelta(days=1) for x in superbowls]


model_results_dict={"MAIN":{'AG':'SUN_AG_AWS.pkl','HF':'SUN_Hot Food_AWS.pkl','RT':'SUN_Retail_AWS.pkl', \
                            'CF':'SUN_Coffee_AWS.pkl','BG':'SUN_Baked Goods_AWS.pkl'}, \
         "WDT":{'AG': 'WED_AG_AWS.pkl'},
         'SDT':{'AG':'SAT_AG_AWS.pkl'},
         "PICO":{'AG':'PICO_AG_AWS.pkl','HF':'PICO_Hot Food_AWS.pkl', \
                            'CF':'PICO_Coffee_AWS.pkl','BG':'PICO_Baked Goods_AWS.pkl'}}


vendor_types={"MAIN":[{'label':"Agricultural", 'value':'AG'},{'label':"Hot Food",'value':'HF'},
                     {'label':"Coffee",'value':'CF'},{'label':"Baked Goods",'value':'BG'},
                     {'label':"Retail",'value':'RT'}],

"PICO":[ {'label':"Agricultural",'value':'AG'},{'label':"Hot Food",'value':'HF'},
                     {'label':"Coffee",'value':'CF'},{'label':"Baked Goods",'value':'BG'}
                     ],

"SDT":[{'label':"Agricultural",'value':'AG'}],

"WDT":[{'label':"Agricultural",'value':'AG'}]}


base_coeff_figure={'data':[{'x':['Market trends','Rain','Wind','Temperature','Holidays','Seasonality'],
        'y':[0]*6,
        'type':'bar'}
        
        ]
            
            ,
            
        'layout': dict(
            xaxis={'title': 'Market Factors'},
            yaxis={'title': 'Relative importance','range':[-50,50]},
            margin={'t': 0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font= {
                'color': 'rgb(255,255,255)','size':15})
        
        }


app = dash.Dash(__name__, external_stylesheets=['style_sheet.css','layout.css'])
application = app.server


app.layout = html.Div(children=[
    
        
    html.Div([
            
            
            
    
    html.Div([
    
    
            html.Div(
            
                    html.H1(
                            children='Seed',
                            style={
                                    'textAlign': 'left'
                                    }
                            )),
            
            html.Div(html.P('Real time sales forecasting for Santa Monica Farmers Markets through social media, public city, and geographical data set merging. \
                           Select your market type and product line below to get weekly forecast estimates.'),style={'marginBottom':20}),
                           


            html.Div(dcc.Dropdown(
                    id='Market Select',
            
                options=[
                    {'label': 'Wednesday Downtown', 'value': 'WDT'},
                    {'label': 'Saturday Downtown', 'value': 'SDT'},
                    {'label': 'Saturday Pico', 'value': 'PICO'},
                    {'label': 'Sunday Main', 'value': 'MAIN'}
                ],
                value='SDT',
                placeholder="Select a market",style={'width': '200px'}
            )),
            
            
    

    html.Div(dcc.Dropdown(
            id='Vendor Select',
            value='AG',
            placeholder="Select a vendor type",style={'width': '200px','marginBottom':20}
            )),
    
    
    
    html.Div(html.H2(children='Select a date')),
            
    html.Div(dcc.DatePickerSingle(
            id='forecast date'))],
            
            className="three columns",style={'marginLeft':30,'marginTop':30}
            ),


    html.Div([
           
            
        html.Div(html.H1(id='forecast output'),style={'marginTop':30,'backgroundColor':'rgb(73,108,145)'}),
        
        
        
        html.Div(dcc.Graph(
                id='Market History'),style={'marginTop':-10,'backgroundColor': 'rgb(60, 60, 60)'}),
            
    
        html.Div(dcc.Graph(
                id='Feature Rank'),style={'marginTop':10,'backgroundColor': 'rgb(60, 60, 60)'})     
                
],className="eight columns")
 ],className='row')


    ])
    
    
@app.callback([Output('forecast output','children'),Output('forecast output','style'),Output('Feature Rank','figure')]
        ,
        [Input('forecast date','date'), Input('Market Select', 'value'), Input('Vendor Select', 'value')])

def output_prediction(forecast_date,selected_market,selected_vendor):

    if forecast_date==None:
        return "Select a date to generate vendor sales forecast", {'color':'rgb(255,255,255)'}, base_coeff_figure
    
    
    df=pd.read_pickle(model_results_dict[selected_market][selected_vendor])
    
    model_params=df.iloc[0]['model_params']
    
    #convert date string to datetime
    
    date_string=forecast_date.split('-')
    date_year=int(date_string[0])
    date_month=int(date_string[1])
    date_day=int(date_string[2])
    forecast_date=datetime.date(date_year,date_month,date_day)
    pred_dates=list(df.iloc[0]['dates'])
    
    if forecast_date.weekday()!=weekday_dict[selected_market][0]:
        return "Select a {} market date to forecast".format(weekday_dict[selected_market][1]), {'color':'rgb(255,255,255)'}, base_coeff_figure
    
    
    #check if date is in the past or future
    
    if forecast_date in pred_dates:
        find_date=0
        for date_item in pred_dates:
            if forecast_date==date_item:
                break
            else:
                find_date+=1
    else:
        find_date=-1
        
    #get prediciton for previous week
    
    last_prediction=df.iloc[0]['dataframe']['Revenue'].iloc[find_date-1]
    
    
    #get weather-related features for week of interest
    offset_time=(forecast_date.year-2014)*365+(forecast_date.month-1)*30+forecast_date.day
    fire_index=df.iloc[0]['dataframe'].iloc[find_date]['Fire Index']
    fm_index=df.iloc[0]['dataframe'].iloc[find_date]['FM Index']
    previous_parking=df.iloc[0]['dataframe'].iloc[find_date]['Previous Parking']
    previous_markets=df.iloc[0]['dataframe'].iloc[find_date]['Previous Markets']
    num_vendors=df.iloc[0]['dataframe'].iloc[find_date]['Num Vendors']
    seasons=math.cos(((forecast_date.month-1)*30+forecast_date.day)/366*math.pi/2)
    
    if (forecast_date in future_forecast_dates) and (forecast_date-timedelta(days=1) in future_forecast_dates):
        temp=current_temp_info[forecast_date]
        wind=current_wind_info[forecast_date]
        rain=np.log(1+current_rain_info[forecast_date])
        previous_rain=np.log(1+current_temp_info[forecast_date-timedelta(days=1)])
    
    else:   
        temp=df.iloc[0]['dataframe'].iloc[find_date]['Temperature']
        wind=df.iloc[0]['dataframe'].iloc[find_date]['Wind']
        rain=df.iloc[0]['dataframe'].iloc[find_date]['Rain']
        previous_rain=df.iloc[0]['dataframe'].iloc[find_date]['Previous Rain']
    
    
    
    
    #get month related features
    
    month_check=[]
    
    for i in range(1,13):
        if i==forecast_date.month:
            month_check.append(1)
        else:
            month_check.append(0)
            
    #get holiday related features
    
    NYD=int(forecast_date in NYE_dates)
    J4=int(forecast_date in july_fourths)
    Christmas=christmas_check(forecast_date)
    Thanksgiving=int(forecast_date in thanksgivings)
    wash_hol=int(forecast_date in wash_days)
    labor_hol=int(forecast_date in labor_days)
    memorial_hol=int(forecast_date in memorial_days)
    mlk_hol=int(forecast_date in mlk_days)
    vet_hol=int(forecast_date in veterans_days)
    sb=int(forecast_date in superbowls)
    
    
    #create a paired feature value/feature name list
    
    feature_names=['Seasons','FM Index','Rain','Num Vendors','Previous Markets','Wind','Temperature','Time Offset','Fire Index','Previous Rain', \
                   'Previous Parking','Christmas','Superbowls','NYE','Thanksgiving','July Fourth','Veterans Day',\
                   'Memorial Day','Wash Day','Labor Day','MLK']+['Is_Jan', 'Is_Feb', 'Is_March',
                  'Is_April', 'Is_May', 'Is_June', 'Is_July', 'Is_August', 'Is_September',
                   'Is_October', 'Is_November', 'Is_December']
                   
                   
    feature_list=[seasons,fm_index,rain,num_vendors,previous_markets,wind,temp,offset_time,fire_index,previous_rain,
                  previous_parking,Christmas,sb,NYD,Thanksgiving,J4,vet_hol,memorial_hol,wash_hol,labor_hol,mlk_hol]+month_check

    
    
    #convert list to dictionary
    
    feature_dict={}
    for i,item in enumerate(feature_names):
        feature_dict[item]=feature_list[i]
    
    
    #get the features used in the model
    model_feature_names=[i[0] for i in model_params] 
    
    #extract only those features for the date of interest
    feature_vector=[]
    for item in model_feature_names:
        feature_vector.append(feature_dict[item])
        
    #format feature list into dataframe
    
    forecast_feature=pd.DataFrame([feature_vector],columns=model_feature_names)[model_feature_names]
    
    #get training set so scaler function can be fit and then used on feature list
    binary_feats=df.iloc[0]['binary features']
    contin_feats=df.iloc[0]['continuous features']
    X_train=df.iloc[0]['feature matrix'].iloc[:-49]
    scaler=preprocessing.StandardScaler().fit(X_train[contin_feats])
    forecast_feature_scaled=np.concatenate((scaler.transform(forecast_feature[contin_feats]),np.array(forecast_feature[binary_feats])),axis=1)
    
    #upload model and make prediciton
    ridge=df.iloc[0]['ridge model']
    prediction=ridge.predict(forecast_feature_scaled)[0]
    
    #now I am going to get the model weights
    coeff_vals=[item[1] for item in model_params]
    feature_coeff_dict={item:coeff_vals[i] for i,item in enumerate(model_feature_names)}
    feature_val_dict = {item: feature_coeff_dict[item]*forecast_feature_scaled[0][i] for i,item in enumerate(contin_feats+binary_feats)}
    
    #extract the holiday/seasonal related features used in the model
    holiday_features=['Christmas','Superbowls','NYE','Thanksgiving','July Fourth','Veterans Day','Memorial Day','Wash Day','Labor Day','MLK']
    holiday_features=[i for i in holiday_features if i in model_feature_names]
    seasonal_features=['Seasons','Is_Jan','Is_Feb','Is_March','Is_April','Is_May','Is_June','Is_July','Is_August','Is_September','Is_October','Is_November','Is_December']
    seasonal_features=[i for i in seasonal_features if i in model_feature_names]
    

    net_holiday_effect=0
    net_seasonal_effect=0
    
    
    #calculate the net effect of different factors
    try:
        for feature in holiday_features:
            net_holiday_effect+=feature_val_dict[feature]
    except:
        
        pass
        
    try:
        for feature in seasonal_features:
            net_seasonal_effect+=feature_val_dict[feature]
    except:
        pass
    
    try:
        wind_features=feature_val_dict['Wind']
    except:
        wind_features=0
    
    
        
    temp_features=feature_val_dict['Temperature']
    rain_features=feature_val_dict['Rain']
    trending_features=feature_val_dict['Previous Markets']
    

    
    
    
    if prediction<last_prediction:
        
        change_describe="weekly decrease"
    else:
        
        change_describe="weekly increase"
        
        
    coeff_df=pd.DataFrame({'features':['Market trends','Rain','Wind','Temperature','Holidays','Seasonality'], \
                  'effect size':[trending_features,rain_features,wind_features,temp_features,net_holiday_effect,net_seasonal_effect],\
                    'color':[trending_features,rain_features,wind_features,temp_features,net_holiday_effect,net_seasonal_effect]})
                
        
    
    coeff_figure={'data':[{'x':coeff_df['features'],
            'y':coeff_df['effect size'],
            'type':'bar',
            'marker':{'color':coeff_df['effect size']}}
            
            ]
                
                ,
                
            'layout': dict(
                xaxis={'title': 'Market Factors'},
                yaxis={'title': 'Relative importance','range':[-50,50]},
                margin={'t': 0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font= {
                    'color': 'rgb(255,255,255)','size':15})
            
            }
            
    return_string="Forecast for {}: ${} ({}% {})".format(forecast_date,round(prediction,2),round(100*(prediction-last_prediction)/last_prediction,2),change_describe)
            
    return_string=html.Div([
    html.H1("Forecast for {}:".format(forecast_date)),
    html.H1("${} ({}% {})".format(round(prediction,2),round(100*(prediction-last_prediction)/last_prediction,2),change_describe))
    ])
                
                
    
    
    return return_string, {'color':'rgb(255,255,255)'},coeff_figure


@app.callback(
    Output('Vendor Select', 'options'),
    [Input('Market Select', 'value')])


def update_select_box(market_select):
            options=vendor_types[market_select]
            return options
        
        
@app.callback(
    Output('Market History', 'figure'),
    [Input('Market Select', 'value'), Input('Vendor Select', 'value') ])

def update_figure(selected_market,selected_vendor):

    df_model=pd.read_pickle(model_results_dict[selected_market][selected_vendor])
    
    
    
    traces=[]
                
            
    traces.append(

                dict(
                    x=df_model['dates'].iloc[0],
                    y=df_model['model predictions'].iloc[0],
                    
                    opacity=0.7,
                    name='Model predictions',
                     marker=dict(
                    color='rgb(255, 128, 0)'))
                )

    
    traces.append(
                dict(
                    x=df_model['dates'].iloc[0],
                    y=df_model['actual sales'].iloc[0],
                    marker=dict(
                    color='rgb(0, 128, 255)'
                ),
                    opacity=.7,
                    name='Actual market sales'))
    
    figure={'data':traces,
            
            'layout':dict(
                    
                    xaxis={'title':'Time'},
                    yaxis={'title':'Average Sales per Vendor'},
                    margin={'l': 80, 'b': 60, 't': 10, 'r': 10},
                
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font= {
                    'color': 'rgb(255,255,255)','size':15},
                    legend={'x': .8, 'y': 1})
            
            }
    
    
    return figure
    
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
    
if __name__ == '__main__':
    application.run(debug=True, host="0.0.0.0", port=82)