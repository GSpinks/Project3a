from flask_wtf import FlaskForm, RecaptchaField
import pandas as pd
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,

)
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length

df = pd.read_csv("stocks.csv")
symbols = df.iloc[:, 0].tolist()
names = df.iloc[:, 1].tolist()
class StockForm(FlaskForm):
    
    symbol = SelectField("Choose Stock Symbol", [DataRequired()],
        choices = [
            (symbols[i], names[i]) for i in range(len(symbols))
        ],
                
    )

    chart_type = SelectField("Choose Chart Type", [DataRequired()],
            choices=[
                ("1", "1. Bar"),
                ("2", "2. Line"),
            ],
        )

    time_series = SelectField("Select Time Series", [DataRequired()],
            choices=[
                ("1", "1. Intraday"),
                ("2", "2. Daily"),
                ("3", "3. Weekly"),
                ("4", "4. Monthly"),
            ],
        )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")
