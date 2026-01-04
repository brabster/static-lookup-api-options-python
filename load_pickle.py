import pickle
import test_harness

def loader(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def parse_value(value):
    return value

default_path = 'uncommitted/recommendations_dataset.pkl'


if __name__ == '__main__':
    test_harness.run_test(default_path, loader)
