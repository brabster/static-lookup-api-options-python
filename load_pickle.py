import pickle
import test_harness

def loader(path):
    with open(path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.pkl", loader)
