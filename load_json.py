import json
import test_harness


def loader(path):
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.jsonl", loader)