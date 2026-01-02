import shelve

import test_harness


def loader(path):
    return shelve.open(path, 'r')


def to_recs_dict(db):
    return db


if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.shelve", loader, to_recs_dict=to_recs_dict)