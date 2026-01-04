import dbm
import json

import test_harness


def loader(path):
    return dbm.open(path, 'r')


def to_recs_dict(db):
    return db


def parse_value(value):
    return json.loads(value)


default_path = 'uncommitted/recommendations_dataset.dbm'

if __name__ == "__main__":
    test_harness.run_test(default_path, loader, to_recs_dict=to_recs_dict, parse_value=parse_value)