import dbm
import json
import zlib
import os

import flask


def load_db(path):
    return dbm.open(path, 'r')


def parse_value(value):
    return json.loads(zlib.decompress(value).decode('utf-8'))


def get_db():
    global db
    if db is None:
        db = load_db(os.environ.get('DB_PATH', 'uncommitted/recommendations_dataset.compressed.dbm'))
    return db

app = flask.Flask(__name__)

db = None

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
