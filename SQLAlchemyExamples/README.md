# Crypto Transaction and Portfolio Tracker

This is a sample app using Flask and SQLAlchemy that tracks a portfolio of crytocurrencies. 

Transactions are entered by hand and there are three pages in total. If you want a more in-depth explanation, I wrote a blog post [here](https://andresberejnoi.com/building-a-simple-flask-app-with-sqlalchemy/).

## How to Run
First, make sure you create a database configuration file called "db_config.yml". Follow the instrucitons in the blog post on how to create it. It is very simple. 

Before running the script, you need to have a database already created. 
To run the script, enter the following command in the terminal:

```sh
python app.py
```

## Previews
The web app has three pages:
- Home
- Portfolio
- Transactions

Here are some screenshots of each.

### Home Page
![](docs/home_page.png)

### Portfolio Page
![](docs/portfolio_page.png)

### Transactions Page
![](docs/transactions_page.png)