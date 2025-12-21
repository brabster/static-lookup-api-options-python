import resource

import pandas

def print_memory_usage_gb():
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return usage / 1024 / 1024

if __name__ == "__main__":

    live = None

    for _ in range(10):
        df = pandas.read_json("uncommitted/recommendations_dataset.json")
            
        live = df
        print(f'{len(live)} records, {print_memory_usage_gb()}GB MaxRSS')

    print_memory_usage_gb()