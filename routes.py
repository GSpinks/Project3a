from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash, Flask

from forms import StockForm
from charts import *

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key' 

@app.route("/", methods=['GET', 'POST'])
@app.route("/stocks", methods=['GET', 'POST'])
def stocks():

    form = StockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            symbol = request.form['symbol']
            chart_type = request.form['chart_type']
            time_series = request.form['time_series']
            start_date = convert_date(request.form['start_date'])
            end_date = convert_date(request.form['end_date'])


            if end_date <= start_date:

                err = "ERROR: End date cannot be earlier than Start date."
                chart = None
            else:
                err = None

                data = get_JSON_data(symbol, time_series, start_date, end_date)
                
                time_series_keys = {
                    "1": "Time Series (5min)",
                    "2": "Time Series (Daily)",
                    "3": "Weekly Time Series",
                    "4": "Monthly Time Series"
                }

                time_series_key = time_series_keys.get(time_series)
                filtered_data = filter_data_by_date(data, start_date, end_date, time_series_key)
                
                if filtered_data:
                    chart = generate_stock_chart(filtered_data, symbol, chart_type)
                else:
                    chart = None
                    err = "No Data Available for the Given Date Range."

            return render_template("stock.html", form=form, template="form-template", err = err, chart = chart)
    
    return render_template("stock.html", form=form, template="form-template")


if __name__ == '__main__':
    app.run(host="0.0.0.0")

app.run(host="0.0.0.0")