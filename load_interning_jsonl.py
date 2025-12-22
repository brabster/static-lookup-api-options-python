import json
import test_harness

from interning_json_decoder import InterningJSONDecoder


def loader(path):
    with open(path, "r") as f:
        data = []
        for line in f:
            data.append(json.loads(line, cls=InterningJSONDecoder))
        return data


if __name__ == "__main__":
    test_harness.run_test("uncommitted/recommendations_dataset.jsonl", loader)