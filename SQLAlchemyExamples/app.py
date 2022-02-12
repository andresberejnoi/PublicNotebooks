# app.py
import os
import pandas as pd
import datetime as dt

from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from flask_bootstrap import Bootstrap

from models import db
from models import Cryptocurrency, Transaction

from forms import TransactionForm

from tools import (generate_uri_from_file,
                   get_id_to_symbol_dict,)
#==========================================
#--------Create Flask app
app = Flask(__name__)

#--------Add URI to flask
database_URI = generate_uri_from_file('db_config.yml')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_URI
 
#need secret key for CSRF from WTF-Forms to work
# you could probably change it to a more secure password
# and store it outside this file
FAKE_SECRET_KEY = 'super_duper_secure_key_1234'   
app.config['SECRET_KEY'] = FAKE_SECRET_KEY

#Setup the app to use Bootstrap in html templates
Bootstrap(app)

# Initialize database and create all tables if they don't exist
db.init_app(app)
with app.app_context():
    db.create_all()
 
#================================================#
#            Routes and API Definition           #
#------------------------------------------------#
@app.route("/",methods=['GET','POST'])
def home():
    form = TransactionForm(request.form)
    form_was_submitted = False

    # we check if the form was submitted
    if request.method == 'POST' and form.validate_on_submit():
        form_was_submitted = True

        #we read data collected from the form
        ticker     = form.ticker.data.upper()
        num_coins  = form.amount.data
        cost_basis = form.cost_basis.data

        #create a Transaction object with data
        tx_obj = Transaction(num_coins, cost_basis)
        
        #retrieve ticker from db or create it if not there
        crypto_obj = db.session.query(Cryptocurrency).filter(Cryptocurrency.ticker==ticker).first()
        if crypto_obj is None:
            crypto_obj = Cryptocurrency(ticker)
            db.session.add(crypto_obj)
            db.session.commit()
        
        #Write new transaction to database
        crypto_obj.transactions.append(tx_obj)
        db.session.add(tx_obj)
        db.session.commit()

    if form_was_submitted:
        return redirect(url_for("home",
                                form=form,))
    else:
        return render_template('home.html',
                               form=form,)
    
@app.route("/portfolio")
def portfolio():

    #get all transactions as a pandas df
    sql_statement = db.session.query(Transaction).statement   #this returns the sql command
    df = pd.read_sql(sql=sql_statement,con=db.session.bind)   #can can retrive the data from the database with pandas.

    grouped_by_coin_df = df[['ticker_id','num_coins','cost_basis']].groupby('ticker_id').sum().reset_index()

    #replace the ticker ids with the actual tickers
    id_to_symbols_dic = get_id_to_symbol_dict(db)

    grouped_by_coin_df = grouped_by_coin_df.replace({'ticker_id':id_to_symbols_dic})

    #get column names and export df as html
    col_names = grouped_by_coin_df.columns.values
    portfolio_tables = [grouped_by_coin_df.to_html(classes='mystyle',index=False),]

    return render_template('portfolio.html',
                           portfolio_tables=portfolio_tables,
                           col_names=col_names,)
 
@app.route("/transactions")
def transactions():
    #gather all transactions in a dataframe
    sql_statement = db.session.query(Transaction).statement
    df = pd.read_sql(sql=sql_statement, con=db.session.bind)

    #replace ticker_id values with actual ticker
    id_to_symbol_dic = get_id_to_symbol_dict(db)
    df = df.replace({'ticker_id':id_to_symbol_dic})

    #Export to HTML
    tables=[df.to_html(classes='mystyle',index=False)]
    col_names=df.columns.values

    return render_template('transactions.html',tables=tables,col_names=col_names)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
