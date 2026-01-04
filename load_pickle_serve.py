import load_pickle as load
import test_harness

import flask

app = flask.Flask(__name__)

db = None

def get_db():
    global db
    if db is None:
        db = test_harness.default_to_recs_dict(load.loader(load.default_path))
    return db

@app.route('/recommendations/<customer_id>', methods=['GET'])
def get_recommendations(customer_id):
    database = get_db()
    try:
        raw_data = database.get(customer_id)
        
        if raw_data is None:
            flask.abort(404, description="Customer not found")
            
        return flask.jsonify(load.parse_value(raw_data))
    except Exception as e:
        app.logger.error(f"Error retrieval: {e}")
        flask.abort(500)
