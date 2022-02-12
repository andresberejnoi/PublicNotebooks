from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()  #our db handler

#--------------------------
# Here we define our models

class Cryptocurrency(db.Model):
    __tablename__ = 'cryptocurrencies'

    id           = db.Column(db.Integer,
                             db.Sequence('cryptocurrencies_id_seq'),
                             primary_key=True)  
    ticker       = db.Column(db.String(32) , 
                             nullable=False, unique=True) 
    last_updated = db.Column(db.DateTime, 
                             server_default=db.func.now(), 
                             onupdate=db.func.now())

    transactions = db.relationship('Transaction', 
                                   backref='cryptocurrencies', 
                                   lazy=True)

    def __init__(self, ticker,):
        self.ticker = ticker
    
    def __repr__(self):
        return f"<Coin: ticker={self.ticker}>"


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id         = db.Column(db.Integer,
                           db.Sequence('transactions_id_seq'),
                           primary_key=True)  
    ticker_id  = db.Column(db.Integer, 
                           db.ForeignKey('cryptocurrencies.id'), 
                           nullable=False)
    num_coins  = db.Column(db.Numeric(19,9, asdecimal=True),
                           nullable=False)
    cost_basis = db.Column(db.Numeric(19,5, asdecimal=True),
                           nullable=False)
    last_updated = db.Column(db.DateTime, 
                             server_default=db.func.now(), 
                             onupdate=db.func.now())

    def __init__(self, num_coins, cost_basis):
        self.num_coins  = num_coins
        self.cost_basis = cost_basis

    def __repr__(self):
        return f"<Transaction: ticker_id={self.ticker_id}, coins={self.num_coins}, cost basis={self.cost_basis}>"