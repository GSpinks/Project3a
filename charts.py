import requests
from datetime import datetime
from datetime import date
import pygal

def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

API_KEY = 'Y5BQFD53B87D4N0O'

def get_JSON_data(symbol, time_series, start_date, end_date):
    if time_series == "1":
        time_string = "TIME_SERIES_INTRADAY"
    elif time_series == "2":
        time_string = "TIME_SERIES_DAILY"
    elif time_series == "3":
        time_string = "TIME_SERIES_WEEKLY"
    else:
        time_string = "TIME_SERIES_MONTHLY"
    
    if time_series == "1":
        url = f'https://www.alphavantage.co/query?function={time_string}&symbol={symbol}&interval=5min&outputsize=full&apikey={API_KEY}'
    else:
        url = f'https://www.alphavantage.co/query?function={time_string}&symbol={symbol}&outputsize=full&apikey={API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    
    return data

def filter_data_by_date(data, start_date, end_date, time_series_key):
    filtered_data = {}
    if time_series_key == "Time Series (5min)":
        for date, values in data[time_series_key].items():
            date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
            if start_date <= date_obj <= end_date:
                filtered_data[date] = values
    else:
        for date, values in data[time_series_key].items():
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            if start_date <= date_obj <= end_date:
                filtered_data[date] = values
    
    return filtered_data

def generate_stock_chart(stock_data, symbol, chart_type):
    dates = []
    closes = []
    opens = []
    highs = []
    lows = []
    
    for date, values in sorted(stock_data.items()):
        dates.append(date)
        closes.append(float(values["4. close"]))
        opens.append(float(values["1. open"]))
        highs.append(float(values["2. high"]))
        lows.append(float(values["3. low"]))

    if chart_type == "2":
        chart = pygal.Line()
        chart.title = f"Stock data for {symbol}"
        chart.x_labels = dates
        chart.add("Close", closes)
        chart.add("Open", opens)
        chart.add("High", highs)
        chart.add("Low", lows)
        return chart.render_data_uri()  
    else:
        chart = pygal.Bar()
        chart.title = f"Stock data for {symbol}"
        chart.x_labels = dates
        chart.add("Close", closes)
        chart.add("Open", opens)
        chart.add("High", highs)
        chart.add("Low", lows)
        return chart.render_data_uri() 