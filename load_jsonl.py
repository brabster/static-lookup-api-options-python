import resource

def print_memory_usage_gb():
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return usage / 1024 / 1024

if __name__ == "__main__":
    import json

    live = None

    for _ in range(10):
        with open("uncommitted/recommendations_dataset.jsonl", "r") as f:
            data = []
            for line in f:
                data.append(json.loads(line))
                
            live = data
            print(f'{len(live)} records, {print_memory_usage_gb()}GB MaxRSS')

    print_memory_usage_gb()