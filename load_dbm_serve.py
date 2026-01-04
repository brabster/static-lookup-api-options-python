import load_dbm as load

import flask

app = flask.Flask(__name__)

db = None

def get_db():
    global db
    if db is None:
        db = load.loader(load.default_path)
    return db

@app.route('/recommendations/<customer_id>', methods=['GET'])
def get_recommendations(customer_id):
    database = get_db()
    try:
        # dbm keys must be bytes or strings. 
        # Verify if your db uses specific encoding for keys.
        raw_data = database.get(customer_id)
        
        if raw_data is None:
            flask.abort(404, description="Customer not found")
            
        return flask.jsonify(load.parse_value(raw_data))
    except Exception as e:
        app.logger.error(f"Error retrieval: {e}")
        flask.abort(500)
