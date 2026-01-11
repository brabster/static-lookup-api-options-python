import dbm
import json
import zlib
import os

import flask

app = flask.Flask(__name__)

db = None

def load_db(path):
    import pathlib
    app.logger.info(f'loading db from {path}...')
    app.logger.info(f'{os.listdir(pathlib.Path(path).parent)}')
    return dbm.open(path, 'r')


def parse_value(value):
    return json.loads(zlib.decompress(value).decode('utf-8'))


def get_db_path():
    return os.environ.get('DB_PATH', 'uncommitted/recommendations_dataset.compressed.dbm')


def get_db():
    global db
    if db is None:
        db = load_db(get_db_path())
    return db


@app.route('/', methods=['GET'])
def index():
    return flask.jsonify({"db_path": get_db_path()})


@app.route('/recommendations/<customer_id>', methods=['GET'])
def get_recommendations(customer_id):
    database = get_db()
    try:
        # dbm keys must be bytes or strings. 
        # Verify if your db uses specific encoding for keys.
        raw_data = database.get(customer_id)
        
        if raw_data is None:
            flask.abort(404, description="Customer not found")
            
        return flask.jsonify(parse_value(raw_data))
    except Exception as e:
        app.logger.error(f"Error retrieval: {e}")
        flask.abort(500)
