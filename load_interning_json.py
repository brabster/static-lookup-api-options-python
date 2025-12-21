import json
import resource

from interning_json_decoder import InterningJSONDecoder

def print_memory_usage_gb():
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return usage / 1024 / 1024

def print_memory_usage_gb():
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(f"Max RSS: {usage / 1024 / 1024} GB")

if __name__ == "__main__":

    data = None

    for _ in range(10):
        with open("uncommitted/recommendations_dataset.json", "r") as f:
            data = json.load(f, cls=InterningJSONDecoder)

        print(len(data))
        print_memory_usage_gb()

    print_memory_usage_gb()