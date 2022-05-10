#===========================
#-- Flask and Flask related imports
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

#===========================
#       Data-Related Imports
import pandas as pd
import cbpro

#===========================
#       Modules
from plotting import create_figure_and_get_components

#==========================================
#--------Create Flask app
app = Flask(__name__)

#-- Setup the app to use Bootstrap in html templates
Bootstrap(app)

def get_price_history(pair) -> pd.DataFrame:
    '''get dataframe of historic BTC prices'''
    public_client = cbpro.PublicClient()
    
    btc_data:list = public_client.get_product_historic_rates(pair, granularity=86400)

    col_names = ['date','open','high','low','close','volume']
    df = pd.DataFrame(btc_data,columns=col_names)
    df = df.set_index('date', drop=True)
    df.index = pd.to_datetime(df.index, unit='s')
    df = df.sort_index()

    return df

#==================================================
# API
@app.route('/', methods=['GET'])
def home():
    #-- get btc data
    trading_pair = 'BTC-USD'
    df_prices = get_price_history(pair=trading_pair)

    # script, div = components(plot)
    script,div = create_figure_and_get_components(df_prices, trading_pair)
    kwargs = {'script': script, 'div': div}
    kwargs['trading_pair'] = trading_pair    

    return render_template('home.html', **kwargs)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
