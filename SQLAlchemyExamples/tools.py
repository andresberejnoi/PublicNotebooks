import yaml

from models import db
from models import Cryptocurrency, Transaction

def generate_uri_from_file(config_file='db_config.yml'):
    with open(config_file, 'r') as f_handle:
        config = yaml.safe_load(f_handle)

    database  = config.get('database')
    username  = config.get('username')
    password  = config.get('password')
    host      = config.get('host')
    port      = config.get('port')
    db_name   = config.get('db_name')

    database_uri = f"{database}://{username}:{password}@{host}:{port}/{db_name}"
    return database_uri

def get_id_to_symbol_dict(db):
    id_to_symbol_map = dict(db.session.query(Cryptocurrency.id,Cryptocurrency.ticker).all())
    return id_to_symbol_map