from wtforms import (SubmitField, StringField,                    
                    DecimalField, validators,)
from flask_wtf import FlaskForm

class TransactionForm(FlaskForm):
    '''Basic form to enter transaction data'''
    ticker = StringField(label="Ticker symbol (i.e. BTC, ETH, ADA, etc): ",
                        validators=[validators.DataRequired()])
    amount = DecimalField(label='Number of coins: ',
                          validators=[validators.DataRequired()],
                          places=9,   #amount of decimal places to accept
                          )
    cost_basis = DecimalField(label='cost basis ($): ',
                              validators=[validators.DataRequired()],
                              places=2,   #amount of decimal places to accept
                              )
    submit = SubmitField('Submit')