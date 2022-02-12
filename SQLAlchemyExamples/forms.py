from wtforms import (SubmitField, StringField,                    
                    DecimalField, validators,)
from flask_wtf import FlaskForm

class TransactionsForm(FlaskForm):
    transactions_str = StringField('Enter string here: (i.e. aapl 0.4 200 -t 10:48, msft 0.5 228 -dt 2020-05-30 13:55)',[validators.DataRequired()]) 
    submit = SubmitField('Submit')

class CostBasisForm(FlaskForm):
    cost_basis = DecimalField(label='cost basis ($): ',
                              validators=[validators.DataRequired()],
                              places=2,   #amount of decimal places to accept
                              )
    submit = SubmitField('Submit')

class CoinAmountForm(FlaskForm):
    amount = DecimalField(label='Number of coins: ',
                          validators=[validators.DataRequired()],
                          places=9,   #amount of decimal places to accept
                          )
    submit = SubmitField('Submit')

class TickerForm(FlaskForm):
    ticker = StringField(label="Ticker symbol (i.e. BTC, ETH, ADA, etc): ",
                        validators=[validators.DataRequired()])
    submit = SubmitField('Submit')